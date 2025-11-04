import sys
import time
import socket
import select
import os

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.DeviceManagerClientRpc import DeviceManagerClient
from kortex_api.autogen.client_stubs.InterconnectConfigClientRpc import InterconnectConfigClient

from kortex_api.autogen.messages import Base_pb2
from kortex_api.autogen.messages import Common_pb2
from kortex_api.autogen.messages import InterconnectConfig_pb2

class UARTBridge:
    def __init__(self, router, ip_address):
        self.router = router
        self.base_ip_address = ip_address

        # Create services
        self.base = BaseClient(self.router)
        self.device_manager = DeviceManagerClient(self.router)
        self.interconnect_config = InterconnectConfigClient(self.router)

        self.interconnect_device_id = self.GetDeviceIdFromDevType(Common_pb2.INTERCONNECT, 0)
        if self.interconnect_device_id is None:
            print("Could not find the Interconnect in the device list, exiting...")
            sys.exit(0)

        self.bridge_socket = None
        self.bridge_id = None

    def GetDeviceIdFromDevType(self, device_type, device_index=0):
        devices = self.device_manager.ReadAllDevices()
        current_index = 0
        for device in devices.device_handle:
            if device.device_type == device_type:
                if current_index == device_index:
                    print(f"Found the Interconnect on device identifier {device.device_identifier}")
                    return device.device_identifier
                current_index += 1
        return None

    def Configure(self, port_id, enabled, speed, word_length, stop_bits, parity):
        uart_config = Common_pb2.UARTConfiguration()
        uart_config.port_id = port_id
        uart_config.enabled = enabled
        uart_config.speed = speed
        uart_config.word_length = word_length
        uart_config.stop_bits = stop_bits
        uart_config.parity = parity

        self.interconnect_config.SetUARTConfiguration(uart_config, deviceId=self.interconnect_device_id)

    def EnableBridge(self):
        self.Cleanup()  # Ensure any previous socket/bridge is closed before enabling a new one

        bridge_config = Base_pb2.BridgeConfig()
        bridge_config.device_identifier = self.interconnect_device_id
        bridge_config.bridgetype = Base_pb2.BRIDGE_TYPE_UART

        bridge_result = self.base.EnableBridge(bridge_config)
        if bridge_result.status != Base_pb2.BRIDGE_STATUS_OK:
            print("EnableBridge failed")
            return False

        self.bridge_id = bridge_result.bridge_id
        config = self.base.GetBridgeConfig(self.bridge_id)
        base_port = config.port_config.out_port

        self.bridge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bridge_socket.connect((self.base_ip_address, base_port))
        self.bridge_socket.setblocking(0)

        print("UART bridge enabled and socket connected.")
        return True

    def send_uart_command(self, data):
        try:
            if isinstance(data, str):
                data = bytes.fromhex(data)
            self.bridge_socket.send(data)
            print(f"[UARTBridge] Sent: {data.hex()}")
        except Exception as e:
            print(f"[UARTBridge] Send error: {e}")

    def DisableBridge(self):
        if self.bridge_id is not None:
            try:
                self.base.DisableBridge(self.bridge_id)
                print("UART bridge disabled")
            except Exception as e:
                print(f"DisableBridge warning (ignored): {e}")
            self.bridge_id = None

    def Cleanup(self):
        if self.bridge_socket:
            try:
                self.bridge_socket.shutdown(socket.SHUT_RDWR)
                self.bridge_socket.close()
                print("UART socket closed")
            except Exception as e:
                print(f"Socket close error: {e}")
            self.bridge_socket = None

        if self.bridge_id is not None:
            self.DisableBridge()


def main():
    import argparse
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities

    parser = argparse.ArgumentParser()
    args = utilities.parseConnectionArguments(parser)

    with utilities.DeviceConnection.createTcpConnection(args) as router:
        bridge = UARTBridge(router, args.ip)

        bridge.Configure(
            InterconnectConfig_pb2.UART_PORT_EXPANSION,
            True,
            Common_pb2.UART_SPEED_115200,
            Common_pb2.UART_WORD_LENGTH_8,
            Common_pb2.UART_STOP_BITS_1,
            Common_pb2.UART_PARITY_NONE
        )

        time.sleep(1)

        if not bridge.EnableBridge():
            return

        print("Enter hex command (e.g., 2B 02 64 00 00 00 23), or 'exit' to quit.")
        while True:
            try:
                user_input = input(">> ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    break
                bridge.send_uart_command(user_input)
            except KeyboardInterrupt:
                break

        bridge.Cleanup()


if __name__ == "__main__":
    main()
