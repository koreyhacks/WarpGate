# WarpGate

An ethical hacking tunneling tool for creating secure connections through firewalls.

![2025-03-12 23_40_55-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/747db014-a560-4250-b0f5-851759239706)


## Description

WarpGate is an ethical hacking tool designed for network penetration testing and security research. It creates tunnels between networks and attempts to bypass firewall restrictions using multiple evasion techniques. Similar to tools like Chisel, WarpGate provides tunneling capabilities with an easy-to-use command-line interface, while offering valuable educational insights into both offensive techniques and defensive measures.

**Features:**
- Client and server mode operation
- Multiple firewall evasion techniques
- Systematic approach to penetration testing
- Educational demonstration of security concepts
- Vibrant animated terminal interface
- Support for multiple simultaneous connections
- Low latency, high performance design

## Installation

### Prerequisites
- Python 3.6+
- Colorama package

### Setup
1. Clone this repository:
```
git clone https://github.com/koreyhacks/warpgate.git
cd warpgate
```

2. Install required dependencies:
```
pip install colorama
```

3. Make the script executable (Linux/Mac):
```
chmod +x warpgate.py
```

## Usage

WarpGate operates in two modes:

### Client Mode
Creates a local listener that forwards traffic to a remote destination:

```
python warpgate.py -c -l 127.0.0.1:8888 -r target.com:80
```

### Server Mode
Creates a relay server that receives connections and forwards them:

```
python warpgate.py -s -l 0.0.0.0:8080 -r internal.service:22
```

### Command Line Options
- `-c`, `--client`: Run in client mode
- `-s`, `--server`: Run in server mode
- `-l`, `--local ADDRESS`: Local address (default: 127.0.0.1:8080)
- `-r`, `--remote ADDRESS`: Remote/target address
- `--no-animation`: Skip the startup animation

## Example: Tunneling RDP to a Windows VM

This example demonstrates tunneling RDP traffic to connect to a Windows VM through WarpGate.

### Setup

1. Ensure both your attack machine (Kali Linux) and target (Windows 10) are running and on the same network.

2. On the Windows 10 VM, ensure Remote Desktop is enabled:
   - Open Settings → System → Remote Desktop
   - Toggle "Enable Remote Desktop" to ON
   - Note your Windows IP address (run `ipconfig` in Command Prompt)

3. On your Kali Linux VM, start WarpGate in client mode:
```
python warpgate.py -c -l 127.0.0.1:9999 -r 10.0.2.6:3389
```
Replace `10.0.2.6` with your Windows VM's actual IP address.

### Connecting via Remmina RDP Client

1. Install Remmina if not already available:
```
sudo apt update
sudo apt install remmina remmina-plugin-rdp
```

2. Open Remmina and create a new connection:
   - Click the "+" button to create a new profile
   - Set Protocol to "RDP"
   - Set Server to "127.0.0.1:9999"
   - Enter your Windows username and password
   - **CRITICAL**: Set Network Connection Type to "LAN" or "Auto" (not "None")
   - Set Color depth to a standard value (16 or 24 bit)
   - Set Security Protocol to "RDP" (not Kerberos/NLA)

3. Click "Save and Connect"

### Troubleshooting

- If you get a "Address already in use" error, try a different port or kill the process using the current port:
```
sudo lsof -i :8888
sudo kill <PID>
```
  
  For stubborn processes that won't terminate with regular kill command, use:
```
sudo kill -9 <PID>
```

- If RDP connection fails, try disabling Network Level Authentication in Windows 10 Remote Desktop settings

- For connection issues, check that your firewall allows RDP traffic on the Windows VM

### How Firewall Evasion Works

WarpGate includes sophisticated firewall evasion techniques that attempt to bypass firewall restrictions:

1. **Multi-Method Connection Approach**: The tool automatically tries several techniques in sequence:
   - Direct connection attempt (if firewall already allows it)
   - Port scanning to find open ports on the target
   - Port knocking sequence to trigger potential dynamic firewall rules
   - IP packet fragmentation techniques to evade packet filtering
   - Connecting through commonly open ports (80, 443, 8080, etc.)
   - Using trusted source ports that are often whitelisted (53, 67, 123)
   - SOCKS-like tunneling through proxy ports

2. **Protocol Adaptation**: WarpGate can:
   - Detect and respond to various tunneling protocols (HTTP CONNECT, SOCKS)
   - Adjust its communication method based on what works with the target firewall
   - Port redirection to reach closed ports via open ones

3. **Completely Automatic Operation**: All evasion techniques happen behind the scenes without requiring user configuration. If one method fails, WarpGate silently tries others until it establishes a connection.

### Firewall Evasion Limitations

It's important to note that modern firewalls like Windows Defender Firewall are designed to be resistant to evasion techniques. WarpGate demonstrates the challenges of bypassing a properly configured firewall:

1. **Security by Design**: A properly configured firewall will block unauthorized connections regardless of the technique used.

2. **Real-World Applications**: In actual penetration testing scenarios, firewall bypass often requires:
   - Finding legitimate applications already allowed through the firewall
   - Exploiting vulnerabilities in exposed services
   - Combining with social engineering or client-side attacks

3. **Educational Value**: The tool provides insight into both offensive techniques and defensive capabilities, making it valuable for security education.

When testing WarpGate against active firewalls, you may observe it systematically attempting all its evasion methods before ultimately reporting that all connection methods failed. This is expected behavior against properly secured systems.

## Results

### Screenshots

#### WarpGate Terminal
![2025-03-12 23_41_48-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/01209818-fe21-46e4-ace5-dff6bf5eebd0)
<br>
*This screenshot shows the WarpGate tool running in a terminal on Kali Linux. You can see the teal and pink gradient logo animation followed by the connection information showing it's listening on 127.0.0.1:9999 and tunneling to the Windows VM's IP address on port 3389. The colorized output indicates the client mode is active and ready to accept connections.*

#### Remmina RDP Client
![2025-03-12 23_43_37-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/7a3b939f-116d-4500-8faf-d7b094504bd5)
<br>
*This screenshot displays the Remmina RDP client configuration with the critical Network Connection Type set to "LAN" or "Auto" instead of "None". You can see the connection parameters including the local tunnel address (127.0.0.1:9999) and authentication settings. This configuration sends the RDP traffic through the WarpGate tunnel.*

#### Firewall Evasion Attempts
![2025-03-13 00_27_58-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/f9714e6c-6d02-4268-8f2c-54a41265c00b)
<br>
*This screenshot shows WarpGate systematically working through its arsenal of firewall evasion techniques. The tool first attempts a direct connection to port 3389, which is blocked by the firewall (shown by the "timed out" message). It then progresses through multiple bypass methods: searching for open ports, executing a port knocking sequence on ports 7000-9000, attempting fragmented packet connections, and finally trying to establish a SOCKS-like tunnel. The red message at the bottom confirms that all evasion methods were ultimately unsuccessful against the properly configured Windows Firewall, demonstrating the effectiveness of modern security measures while showcasing WarpGate's methodical approach to penetration testing.*

#### If Successful
![2025-03-12 23_46_41-KALI  Running  - Oracle VirtualBox _ 1](https://github.com/user-attachments/assets/39c9e70d-cabf-4713-b922-7544b9010561)
<br>
*This screenshot shows a successful connection to the remote host.*

## Security Considerations

WarpGate is designed for ethical hacking, security research, and legitimate penetration testing. Only use this tool on systems you own or have explicit permission to test. Unauthorized use against third-party systems may violate computer crime laws.

### Educational Value

WarpGate demonstrates important security concepts:

1. **Offensive Techniques**: The tool showcases various methods attackers might use to bypass network restrictions.

2. **Defensive Effectiveness**: When used against properly configured firewalls, it demonstrates the effectiveness of modern security measures.

3. **Security Awareness**: The tool helps security professionals understand both attack vectors and defense mechanisms.

This balanced approach makes WarpGate valuable for cybersecurity education, providing insights into both offensive and defensive aspects of network security.

## Author

Created by koreyhacks_
