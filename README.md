# Kinova Bionic Hand Control System

A comprehensive robotics control system for Kinova robotic arms integrated with bionic hand prosthetics. This project enables real-time finger movement control and manipulation through UART communication bridges and intuitive UI interfaces.

## 📋 Project Overview

This project was developed during a BARC (Bionics and Robotics Center) internship and demonstrates advanced robotics programming with hardware integration, real-time control systems, and communication protocols.

### Key Features

- **UART Bridge Communication**: Seamless serial communication between robotic arms and bionic hand actuators
- **Real-time Finger Control**: Direct finger movement manipulation through command protocols
- **Device Management**: Automatic device discovery and configuration using Kortex API
- **Session Management**: Secure authenticated connections with timeout handling
- **Command Processing**: Hex-based command transmission and receipt
- **Network Communication**: TCP/UDP transport protocols for device connectivity
- **Graphical User Interface**: PyQt-based UI for intuitive control and monitoring
- **Utilities Framework**: Reusable connection and configuration utilities

## 🛠️ Technology Stack

### Core Technologies
- **Language**: Python 3.x
- **Framework**: Kortex API (Kinova Robot Manipulation Framework)
- **GUI Framework**: PyQt/Qt Designer
- **Communication Protocols**: UART, TCP, UDP
- **Hardware**: Kinova Robot Arms, Bionic Hand Prosthetics

### Dependencies
- `kortex_api` - Kinova Kortex API for robot control
- `socket` - Network socket programming
- `PyQt5` - GUI framework (if using UI files)
- `argparse` - Command-line argument parsing
- Python standard libraries: `sys`, `time`, `os`, `select`, `threading`

### APIs & SDKs Used
- **Kortex Base API**: Robot base commands and control
- **Device Manager API**: Device discovery and management
- **Interconnect Config API**: UART configuration
- **Session Manager**: Authentication and session handling

## 📁 Project Structure

```
kinova-bionic-hand-control/
├── uart_bridge.py                 # Core UART bridge implementation
├── 01-uart_bridge.py              # Enhanced UART bridge version
├── utilities.py                   # Connection and utilities module
├── ui_form.py                     # Generated PyQt UI code
├── widget.py                      # Custom widget implementations
├── form.ui                        # Qt Designer UI file
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
│
├── certificates/                  # Internship credentials
│   ├── README.md
│   └── BARC_Internship_Certificate.pdf
│
└── untitled2.pyproject            # PyCharm project configuration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Kinova Kortex SDK installed
- PyQt5 (if using GUI)
- Access to Kinova robot arm with bionic hand module
- Network connectivity to robot (TCP/UDP ports 10000-10001)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kinova-bionic-hand-control.git
   cd kinova-bionic-hand-control
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Kinova SDK**
   - Install Kortex API as per Kinova documentation
   - Ensure robot is powered and network-accessible

### Configuration

Update connection parameters in `utilities.py`:

```python
parser.add_argument("--ip", type=str, help="IP address of destination", default="192.168.1.10")
parser.add_argument("-u", "--username", type=str, help="username to login", default="admin")
parser.add_argument("-p", "--password", type=str, help="password to login", default="admin")
```

## 💻 Usage

### Using Command Line (UART Bridge)

```bash
python uart_bridge.py --ip 192.168.1.10 -u admin -p admin
```

### Using Enhanced Version

```bash
python 01-uart_bridge.py --ip 192.168.1.10 -u admin -p admin
```

### Using GUI (If PyQt UI is set up)

```bash
python widget.py
```

### Command Format

Send hexadecimal commands to control bionic hand fingers:

```
>> 2B 02 64 00 00 00 23
[UARTBridge] Sent: 2b0264000000023
```

### Example Control Sequence

```python
from uart_bridge import UARTBridge
import utilities

# Create connection
args = utilities.parseConnectionArguments()
with utilities.DeviceConnection.createTcpConnection(args) as router:
    bridge = UARTBridge(router, args.ip)
    
    # Configure UART
    if bridge.EnableBridge():
        # Send finger control command
        bridge.send_uart_command("2B 02 64 00 00 00 23")
    
    bridge.Cleanup()
```

## 🔧 Core Components

### UARTBridge Class

Manages UART communication with bionic hand through Kinova interconnect module.

**Key Methods:**
- `__init__(router, ip_address)` - Initialize bridge with router and IP
- `Configure()` - Set UART parameters
- `EnableBridge()` - Establish UART bridge connection
- `send_uart_command()` - Send hex commands
- `DisableBridge()` - Disable bridge
- `Cleanup()` - Cleanup resources

### DeviceConnection Class

Handles TCP/UDP connections with authentication.

**Features:**
- Automatic device discovery
- Session management with timeout handling
- TCP (1kHz) and UDP (10kHz) transport options
- Secure credential-based authentication

### UI Components

- `ui_form.py` - PyQt-generated UI code
- `widget.py` - Custom widget implementations
- `form.ui` - Qt Designer UI file for visual editing

## ⚙️ Configuration Options

### Robot Connection
- IP Address: `192.168.1.10` (default)
- TCP Port: `10000`
- UDP Port: `10001`

### UART Parameters
- Baud Rate: `115200`
- Data Bits: `8`
- Stop Bits: `1`
- Parity: `None`

### Credentials
- Default Username: `admin`
- Default Password: `admin`

## 🏆 Internship & Credentials

This project was developed during my **BARC Internship** (Bionics and Robotics Center).

[View Internship Certificate](./certificates)

### Certificate Details
- **Organization**: BARC (Bionics and Robotics Center)
- **Program**: Robotics & Hardware Integration
- **Certificate**: [BARC_Internship_Certificate.pdf](./certificates/BARC_Internship_Certificate.pdf)

## 🐛 Troubleshooting

### Connection Issues
```
Error: Could not find the Interconnect in the device list
Solution: Verify bionic hand module is properly connected and powered
```

### UART Communication Failure
```
Error: [UARTBridge] Send error
Solution: Check baud rate, verify UART device is enabled, check cable connections
```

### Authentication Errors
```
Error: Logging failed
Solution: Verify username/password, check network connectivity to robot
```

## 📊 Performance Metrics

- **Command Latency**: < 100ms
- **UART Baudrate**: 115200 bps
- **Network Transport Speed**: 
  - TCP: 1 kHz (1000 commands/sec)
  - UDP: 10 kHz (10000 commands/sec)
- **Session Timeout**: 10 seconds inactivity

## 📚 Documentation

- **Kinova Kortex API**: [Official Documentation](https://docs.kinovarobotics.com/)
- **Internship Report**: See `certificates/` folder
- **Qt Designer Guide**: For UI modifications, use Qt Designer with `form.ui`

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see `LICENSE` file for details.

## 👤 Author

**Subodh Kumar Sahu**
- GitHub: [SubodhKumarSahu2826](https://github.com/SubodhKumarSahu2826)
- LinkedIn: [Subodh Kumar Sahu](https://www.linkedin.com/in/subodhkumarsahu98/)

## 🙏 Acknowledgments

- **BARC (Bionics and Robotics Center)** for internship opportunity
- **Kinova Robotics** for Kortex API and documentation
- **Research Mentors** for guidance and support

## 📞 Support

For support, issues, or questions:
- Open an issue on GitHub
- Check documentation in the project

## 🔮 Future Enhancements

- [ ] Real-time haptic feedback integration
- [ ] Machine learning-based finger movement prediction
- [ ] Web-based control interface
- [ ] Mobile app for remote control
- [ ] Advanced gesture recognition
- [ ] Multi-hand coordination
- [ ] Simulation environment integration
- [ ] ROS (Robot Operating System) integration

---

**Last Updated**: August 2025  
**Status**: Active Development  
**Version**: 2.0.0
