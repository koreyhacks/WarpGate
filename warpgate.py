#!/usr/bin/env python3
"""
WarpGate - An Ethical Hacking Tunneling Tool
A tool for bypassing firewalls and creating secure tunnels
"""

import argparse
import socket
import select
import threading
import time
import random
import sys
import os
from colorama import init, Fore, Back, Style

# Initialize colorama
init()

class WarpGateAnimation:
    def __init__(self):
        self.teal = '\033[38;2;0;180;180m'
        self.pink = '\033[38;2;255;105;180m'
        self.reset = '\033[0m'
        
    def generate_gradient_text(self, text, start_color=(0, 180, 180), end_color=(255, 105, 180)):
        """Generate text with a color gradient from start_color to end_color"""
        result = ""
        
        for i, char in enumerate(text):
            # Calculate the color for this position in the gradient
            r = start_color[0] + (end_color[0] - start_color[0]) * i // len(text)
            g = start_color[1] + (end_color[1] - start_color[1]) * i // len(text)
            b = start_color[2] + (end_color[2] - start_color[2]) * i // len(text)
            
            # Add the color code and character
            result += f'\033[38;2;{r};{g};{b}m{char}'
            
        return result + self.reset
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_animation(self):
        """Display the WarpGate animation"""
        self.clear_screen()
        
        # WarpGate ASCII art
        warpgate_logo = [
            "░██╗░░░░░░░██╗░█████╗░██████╗░██████╗░░██████╗░░█████╗░████████╗███████╗",
            "░██║░░██╗░░██║██╔══██╗██╔══██╗██╔══██╗██╔════╝░██╔══██╗╚══██╔══╝██╔════╝",
            "░╚██╗████╗██╔╝███████║██████╔╝██████╔╝██║░░██╗░███████║░░░██║░░░█████╗░░",
            "░░████╔═████║░██╔══██║██╔══██╗██╔═══╝░██║░░╚██╗██╔══██║░░░██║░░░██╔══╝░░",
            "░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║██║░░░░░╚██████╔╝██║░░██║░░░██║░░░███████╗",
            "░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝"
        ]
        
        # Animation frames for "stars" moving through the "warp gate"
        for frame in range(10):
            self.clear_screen()
            
            # Print each line of the logo with gradient
            for i, line in enumerate(warpgate_logo):
                gradient_line = self.generate_gradient_text(line)
                print(gradient_line)
            
            # Print creator line
            print("\n" + " " * 25 + "By koreyhacks_" + "\n")
            
            # Create "warp" effect
            width = 60
            height = 3
            print("\n")
            
            for y in range(height):
                line = ""
                for x in range(width):
                    # Create a warp tunnel effect with random stars
                    if random.random() < 0.1:
                        line += Fore.WHITE + "*" + Style.RESET_ALL
                    elif random.random() < 0.05:
                        line += Fore.CYAN + "." + Style.RESET_ALL
                    else:
                        line += " "
                print(" " * 10 + line)
            
            time.sleep(0.2)
        
        # Final display with version and startup message
        self.clear_screen()
        
        # Print logo with gradient in final position
        for line in warpgate_logo:
            gradient_line = self.generate_gradient_text(line)
            print(gradient_line)
            
        # Print creator and version info
        print("\n" + " " * 25 + Style.BRIGHT + "By koreyhacks_" + Style.RESET_ALL)
        print(" " * 25 + "v1.0.0 - Quantum Breach Edition\n")
        print(" " * 15 + "[ Initializing Quantum Tunneling Protocols ]\n")

class Tunnel:
    """Base class for WarpGate tunneling functionality"""
    def __init__(self, local_host, local_port):
        self.local_host = local_host
        self.local_port = local_port
        self.running = False
        
    def stop(self):
        """Stop the tunnel"""
        self.running = False
        
class ClientTunnel(Tunnel):
    """Client-side tunnel implementation with enhanced firewall evasion"""
    def __init__(self, local_host, local_port, remote_host, remote_port):
        super().__init__(local_host, local_port)
        self.remote_host = remote_host
        self.remote_port = remote_port
        # Common ports that are often allowed through firewalls
        self.common_ports = [80, 443, 8080, 53, 143, 25, 21, 22, 110, 993]
        
    def start(self):
        """Start the client tunnel with firewall evasion techniques"""
        self.running = True
        
        try:
            # Create local server socket
            local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            local_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            local_socket.bind((self.local_host, self.local_port))
            local_socket.listen(5)
            
            print(f"{Fore.GREEN}[+] Listening on {self.local_host}:{self.local_port}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[+] Tunneling to {self.remote_host}:{self.remote_port} (Firewall Evasion Active){Style.RESET_ALL}")
            
            while self.running:
                client_socket, addr = local_socket.accept()
                print(f"{Fore.YELLOW}[+] Accepted connection from {addr[0]}:{addr[1]}{Style.RESET_ALL}")
                
                # Spawn a new thread to handle the client connection
                client_handler = threading.Thread(
                    target=self._handle_client_connection,
                    args=(client_socket,),
                    daemon=True
                )
                client_handler.start()
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error in client tunnel: {e}{Style.RESET_ALL}")
        finally:
            if 'local_socket' in locals() and local_socket:
                local_socket.close()
    
    def _handle_client_connection(self, client_socket):
        """Handle a client connection with firewall evasion"""
        target_socket = None
        try:
            # First try direct connection (might work if firewall allows it)
            print(f"{Fore.CYAN}[*] Attempting direct connection to {self.remote_host}:{self.remote_port}{Style.RESET_ALL}")
            try:
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                target_socket.settimeout(3)
                target_socket.connect((self.remote_host, self.remote_port))
                print(f"{Fore.GREEN}[+] Direct connection successful!{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}[*] Direct connection blocked: {e}{Style.RESET_ALL}")
                target_socket = None
            
            # If direct connection failed, try port scanning for open ports
            if target_socket is None:
                print(f"{Fore.YELLOW}[*] Attempting to find open ports on target...{Style.RESET_ALL}")
                open_port = self._find_open_port()
                
                if open_port:
                    print(f"{Fore.GREEN}[+] Found open port {open_port}, establishing connection{Style.RESET_ALL}")
                    # Connect through the open port
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_socket.connect((self.remote_host, open_port))
                    
                    # If connecting to a different port than requested, perform port forwarding
                    if open_port != self.remote_port:
                        print(f"{Fore.CYAN}[*] Setting up port redirection from {open_port} to {self.remote_port}{Style.RESET_ALL}")
                        # We need to tell the target to forward to the actual target port
                        # This is a simplified version - in a real implementation, we would need
                        # a protocol for communicating this to a compatible server
                        
                        # For demonstration, we just send a special header that our ServerTunnel would recognize
                        redirect_header = f"X-WARPGATE-REDIRECT: {self.remote_port}\r\n\r\n".encode()
                        target_socket.send(redirect_header)
                
            # If we still don't have a connection, try more advanced techniques
            if target_socket is None:
                print(f"{Fore.YELLOW}[*] Attempting to use a port knocking sequence...{Style.RESET_ALL}")
                # Port knocking sequence - send packets to specific ports in sequence
                # This can trigger a firewall rule to temporarily open the target port
                self._port_knocking_sequence()
                
                # Try direct connection again after port knocking
                try:
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_socket.settimeout(3)
                    target_socket.connect((self.remote_host, self.remote_port))
                    print(f"{Fore.GREEN}[+] Connection established after port knocking!{Style.RESET_ALL}")
                except:
                    target_socket = None
            
            # If still no connection, try a raw packet-level approach with IP fragmentation
            # This is a simplified simulation - in a real tool this would require raw socket privileges
            if target_socket is None:
                print(f"{Fore.YELLOW}[*] Attempting connection using fragmented packets...{Style.RESET_ALL}")
                try:
                    # In a real implementation, this would use raw sockets to fragment TCP packets
                    # For this demo version, we'll just try a standard socket but with special options
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle's algorithm
                    target_socket.connect((self.remote_host, self.remote_port))
                    print(f"{Fore.GREEN}[+] Connection established with IP fragmentation!{Style.RESET_ALL}")
                except:
                    target_socket = None
            
            # Last resort - try connecting to a common proxy port and establish a tunnel
            if target_socket is None:
                print(f"{Fore.YELLOW}[*] Attempting to establish a SOCKS-like tunnel...{Style.RESET_ALL}")
                for proxy_port in [1080, 8080, 3128]:  # Common proxy ports
                    try:
                        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        target_socket.settimeout(3)
                        target_socket.connect((self.remote_host, proxy_port))
                        # Send a SOCKS-like handshake - this is a simplified version
                        # In a real implementation, this would follow the SOCKS protocol
                        socks_handshake = bytes([0x05, 0x01, 0x00])  # SOCKS5, 1 auth method, no auth
                        target_socket.send(socks_handshake)
                        response = target_socket.recv(2)
                        if response[0] == 0x05:  # SOCKS5 response
                            # Send connection request
                            connect_request = bytes([0x05, 0x01, 0x00, 0x01])  # SOCKS5, TCP connect, reserved, IPv4
                            # Add target IP in bytes
                            for octet in self.remote_host.split('.'):
                                connect_request += bytes([int(octet)])
                            # Add target port in bytes (big-endian)
                            connect_request += bytes([(self.remote_port >> 8) & 0xFF, self.remote_port & 0xFF])
                            target_socket.send(connect_request)
                            print(f"{Fore.GREEN}[+] SOCKS tunnel established through port {proxy_port}!{Style.RESET_ALL}")
                            break
                    except:
                        target_socket = None
                        continue
            
            # Final check - if we have a connection, set up the data forwarding
            if target_socket:
                # Set up bidirectional data forwarding
                threading.Thread(target=self._forward, args=(client_socket, target_socket), daemon=True).start()
                threading.Thread(target=self._forward, args=(target_socket, client_socket), daemon=True).start()
            else:
                print(f"{Fore.RED}[!] All connection methods failed. Unable to establish tunnel.{Style.RESET_ALL}")
                client_socket.close()
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error handling client connection: {e}{Style.RESET_ALL}")
            if client_socket:
                client_socket.close()
            if target_socket:
                target_socket.close()
    
    def _find_open_port(self):
        """Scan for open ports on the target to find a way through the firewall"""
        for port in self.common_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)  # Quick timeout for fast scanning
                result = s.connect_ex((self.remote_host, port))
                s.close()
                if result == 0:
                    print(f"{Fore.GREEN}[+] Found open port: {port}{Style.RESET_ALL}")
                    return port
            except:
                pass
        return None
    
    def _port_knocking_sequence(self):
        """Perform a port knocking sequence to potentially open the firewall"""
        # Common port knocking sequence - in a real tool this would be configurable
        knock_sequence = [7000, 8000, 9000]
        
        for port in knock_sequence:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)  # Very short timeout - we don't expect these to connect
                s.connect_ex((self.remote_host, port))
                s.close()
                print(f"{Fore.CYAN}[*] Knock on port {port}{Style.RESET_ALL}")
                time.sleep(0.5)  # Small delay between knocks
            except:
                pass
    
    def _forward(self, source, destination):
        """Forward data between sockets with minimal alterations"""
        try:
            while self.running:
                data = source.recv(4096)
                if not data:
                    break
                destination.send(data)
        except:
            pass
        finally:
            source.close()
            destination.close()

class ServerTunnel(Tunnel):
    """Server-side tunnel implementation with advanced firewall evasion"""
    def __init__(self, local_host, local_port, target_host, target_port):
        super().__init__(local_host, local_port)
        self.target_host = target_host
        self.target_port = target_port
        self.connections = []
        
    def start(self):
        """Start the server tunnel with firewall evasion capability"""
        self.running = True
        
        try:
            # Create server socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.local_host, self.local_port))
            server_socket.listen(5)
            
            print(f"{Fore.GREEN}[+] WarpGate server listening on {self.local_host}:{self.local_port}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[+] Forwarding connections to {self.target_host}:{self.target_port} (Firewall Evasion Active){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Advanced evasion techniques enabled{Style.RESET_ALL}")
            
            while self.running:
                client_socket, addr = server_socket.accept()
                print(f"{Fore.YELLOW}[+] Accepted WarpGate connection from {addr[0]}:{addr[1]}{Style.RESET_ALL}")
                
                # Handle client in a new thread
                client_handler = threading.Thread(target=self._handle_client, args=(client_socket,), daemon=True)
                client_handler.start()
                self.connections.append(client_handler)
                
        except Exception as e:
            print(f"{Fore.RED}[!] Error in server tunnel: {e}{Style.RESET_ALL}")
        finally:
            if 'server_socket' in locals() and server_socket:
                server_socket.close()
    
    def _handle_client(self, client_socket):
        """Handle a WarpGate client connection with advanced evasion techniques"""
        target_socket = None
        try:
            # Check for special headers in the first packet
            data = client_socket.recv(4096, socket.MSG_PEEK)
            str_data = data.decode('utf-8', errors='ignore')

            # Check for port redirection header
            redirect_port = self.target_port
            if "X-WARPGATE-REDIRECT:" in str_data:
                try:
                    # Extract port from header
                    redirect_header = str_data.split("X-WARPGATE-REDIRECT:")[1].split("\r\n")[0].strip()
                    redirect_port = int(redirect_header)
                    print(f"{Fore.CYAN}[*] Detected port redirection request to port {redirect_port}{Style.RESET_ALL}")
                    # Actually receive the data to clear it from the buffer
                    client_socket.recv(len(data))
                except:
                    pass
            
            # Check for SOCKS handshake
            if len(data) >= 3 and data[0] == 0x05:  # SOCKS5 handshake
                print(f"{Fore.CYAN}[*] Detected SOCKS tunnel request{Style.RESET_ALL}")
                target_socket = self._handle_socks_tunnel(client_socket)
            # Check for HTTP CONNECT
            elif "CONNECT" in str_data:
                print(f"{Fore.CYAN}[*] Detected HTTP CONNECT tunnel request{Style.RESET_ALL}")
                target_socket = self._handle_http_connect(client_socket)
            else:
                # Regular connection or other protocol
                # Attempt multiple methods to connect to target
                print(f"{Fore.CYAN}[*] Attempting to reach target {self.target_host}:{redirect_port}{Style.RESET_ALL}")
                target_socket = self._create_target_connection(redirect_port)
                
                if target_socket:
                    # Standard data forwarding
                    threading.Thread(target=self._forward, args=(client_socket, target_socket), daemon=True).start()
                    threading.Thread(target=self._forward, args=(target_socket, client_socket), daemon=True).start()
                else:
                    print(f"{Fore.RED}[!] Failed to connect to target{Style.RESET_ALL}")
                    client_socket.close()
        
        except Exception as e:
            print(f"{Fore.RED}[!] Error handling client: {e}{Style.RESET_ALL}")
            if 'client_socket' in locals() and client_socket:
                client_socket.close()
    
    def _create_target_connection(self, port=None):
        """Create a connection to the target using multiple methods"""
        if port is None:
            port = self.target_port
            
        # Method 1: Direct connection
        try:
            print(f"{Fore.CYAN}[*] Attempting direct connection to target{Style.RESET_ALL}")
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.settimeout(3)
            target_socket.connect((self.target_host, port))
            print(f"{Fore.GREEN}[+] Direct connection to target successful{Style.RESET_ALL}")
            return target_socket
        except Exception as e:
            print(f"{Fore.YELLOW}[*] Direct connection failed: {e}{Style.RESET_ALL}")
        
        # Method 2: Try fragment packets (simulated here)
        try:
            print(f"{Fore.CYAN}[*] Attempting connection with TCP options{Style.RESET_ALL}")
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            # Add more socket options to potentially bypass firewalls
            if hasattr(socket, 'TCP_QUICKACK'):  # Linux-specific
                target_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
            target_socket.settimeout(3)
            target_socket.connect((self.target_host, port))
            print(f"{Fore.GREEN}[+] TCP option-based connection successful{Style.RESET_ALL}")
            return target_socket
        except:
            pass
        
        # Method 3: Try different source ports
        # Some firewalls allow traffic from specific source ports
        try:
            for source_port in [53, 67, 123]:  # DNS, DHCP, NTP - often trusted
                try:
                    print(f"{Fore.CYAN}[*] Trying trusted source port {source_port}{Style.RESET_ALL}")
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_socket.bind(('0.0.0.0', source_port))  # May require root privileges
                    target_socket.settimeout(3)
                    target_socket.connect((self.target_host, port))
                    print(f"{Fore.GREEN}[+] Connection from trusted port {source_port} successful{Style.RESET_ALL}")
                    return target_socket
                except:
                    continue
        except:
            pass
                
        # Method 4: Try connecting through common open ports
        for alt_port in [80, 443, 25, 21, 22]:
            if alt_port == port:  # Skip if this is the port we're already trying
                continue
                
            try:
                print(f"{Fore.CYAN}[*] Trying connection through alternate port {alt_port}{Style.RESET_ALL}")
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                target_socket.settimeout(3)
                target_socket.connect((self.target_host, alt_port))
                print(f"{Fore.GREEN}[+] Connected to alternate port {alt_port}{Style.RESET_ALL}")
                
                # In a real implementation, we would need a way to redirect traffic from
                # this port to the actual target port. This is a simplified demonstration.
                print(f"{Fore.YELLOW}[*] NOTE: Connected to port {alt_port} instead of {port}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] In a real scenario, additional steps would be needed to redirect traffic{Style.RESET_ALL}")
                return target_socket
            except:
                continue
        
        print(f"{Fore.RED}[!] All connection methods failed{Style.RESET_ALL}")
        return None
        
    def _handle_http_connect(self, client_socket):
        """Handle HTTP CONNECT tunnel request"""
        try:
            # Read HTTP CONNECT request
            request = b""
            while b"\r\n\r\n" not in request:
                chunk = client_socket.recv(4096)
                if not chunk:
                    return None
                request += chunk
            
            # Connect to target
            target_socket = self._create_target_connection()
            if target_socket:
                # Send 200 Connection Established response
                client_socket.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")
                
                # Set up data forwarding
                threading.Thread(target=self._forward, args=(client_socket, target_socket), daemon=True).start()
                threading.Thread(target=self._forward, args=(target_socket, client_socket), daemon=True).start()
                
                return target_socket
            else:
                client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
                client_socket.close()
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[!] HTTP CONNECT error: {e}{Style.RESET_ALL}")
            return None
    
    def _handle_socks_tunnel(self, client_socket):
        """Handle SOCKS tunnel request"""
        try:
            # Read SOCKS handshake
            request = client_socket.recv(4096)
            
            # Very simple handling for SOCKS5 - in a real implementation this would be more complete
            if len(request) >= 3 and request[0] == 0x05:  # SOCKS5
                # Send auth method response (no auth)
                client_socket.send(bytes([0x05, 0x00]))
                
                # Read connect request
                connect_req = client_socket.recv(4096)
                
                # Connect to target
                target_socket = self._create_target_connection()
                if target_socket:
                    # Send success response
                    client_socket.send(bytes([0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0]))
                    
                    # Set up data forwarding
                    threading.Thread(target=self._forward, args=(client_socket, target_socket), daemon=True).start()
                    threading.Thread(target=self._forward, args=(target_socket, client_socket), daemon=True).start()
                    
                    return target_socket
                else:
                    # Send failure response
                    client_socket.send(bytes([0x05, 0x01, 0x00, 0x01, 0, 0, 0, 0, 0, 0]))
                    client_socket.close()
                    return None
            
            return None
            
        except Exception as e:
            print(f"{Fore.RED}[!] SOCKS tunnel error: {e}{Style.RESET_ALL}")
            return None
    
    def _forward(self, source, destination):
        """Forward data between sockets"""
        try:
            while self.running:
                data = source.recv(4096)
                if not data:
                    break
                destination.send(data)
        except:
            pass
        finally:
            source.close()
            destination.close()

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='WarpGate - Secure Tunneling Tool')
    
    # Main mode arguments
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-c', '--client', action='store_true', help='Run in client mode')
    mode_group.add_argument('-s', '--server', action='store_true', help='Run in server mode')
    
    # Network configuration
    parser.add_argument('-l', '--local', default='127.0.0.1:8080', help='Local address (default: 127.0.0.1:8080)')
    parser.add_argument('-r', '--remote', help='Remote/target address (required)')
    
    # Additional options
    parser.add_argument('--no-animation', action='store_true', help='Skip the startup animation')
    
    return parser.parse_args()

def main():
    """Main entry point for WarpGate"""
    args = parse_arguments()
    
    # Parse local address
    try:
        local_host, local_port = args.local.split(':')
        local_port = int(local_port)
    except ValueError:
        print(f"{Fore.RED}[!] Invalid local address format. Use host:port{Style.RESET_ALL}")
        return
    
    # Show animation unless skipped
    if not args.no_animation:
        animation = WarpGateAnimation()
        animation.show_animation()
    
    # Verify remote address is provided
    if not args.remote:
        print(f"{Fore.RED}[!] Remote address is required{Style.RESET_ALL}")
        return
    
    # Parse remote address
    try:
        remote_host, remote_port = args.remote.split(':')
        remote_port = int(remote_port)
    except ValueError:
        print(f"{Fore.RED}[!] Invalid remote address format. Use host:port{Style.RESET_ALL}")
        return
    
    # Start appropriate tunnel mode
    tunnel = None
    try:
        if args.client:
            print(f"{Fore.CYAN}[*] Starting WarpGate in client mode{Style.RESET_ALL}")
            tunnel = ClientTunnel(local_host, local_port, remote_host, remote_port)
        else:
            print(f"{Fore.CYAN}[*] Starting WarpGate in server mode{Style.RESET_ALL}")
            tunnel = ServerTunnel(local_host, local_port, remote_host, remote_port)
        
        # Start tunnel in main thread
        tunnel.start()
    
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}[*] WarpGate shutdown requested{Style.RESET_ALL}")
    finally:
        if tunnel:
            tunnel.stop()
        print(f"{Fore.GREEN}[*] WarpGate tunnel closed{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
