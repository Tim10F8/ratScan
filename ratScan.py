#!/usr/bin/python3
# Interactive Port Scanner with Threading, Output Saving, Colorized Output, Service Detection.

import socket
import argparse
import threading
import time
from datetime import datetime

# ANSI escape codes for text color
GREEN = "\033[92m"
RESET = "\033[0m"

# Define a lock to ensure thread-safe printing
print_lock = threading.Lock()

# ASCII art of a rat
RAT_ASCII_ART = """
  ()-()   
   \\"/ 
    `
"""

# Function to get service name based on port number
def get_service(port, protocol):
    try:
        service_name = socket.getservbyport(port, protocol)
        return service_name
    except OSError:
        return "Unknown"

# Function to scan a single port on the target IP address
def scan_port(target, port, protocol, scanned_ports, output_file=None, rate_limit=None):
    try:
        # Create a socket object
        if protocol == 'tcp':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol == 'udp':
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print("Invalid protocol. Please choose TCP or UDP.")
            return

        socket.setdefaulttimeout(1)
        s.connect((target, port))

        with print_lock:
            if port not in scanned_ports:
                service = get_service(port, protocol)
                print(f"Port {port}/{protocol.upper()} ({service}) is {GREEN}open{RESET}")
                scanned_ports.add(port)

        s.close()

    except Exception as e:
        pass  # Ignore errors

    # Apply rate limit if specified
    if rate_limit:
        time.sleep(rate_limit)

# Function to scan multiple ports on the target IP address using threading
def scan_ports(target, ports, protocol, num_threads, output_file=None, rate_limit=None):
    # Print ASCII art of a rat in green
    print(f"{GREEN}{RAT_ASCII_ART}{RESET}")

    # Add a banner
    print(GREEN + "-" * 50)
    print(f"Scanning target: {target}")
    print(f"Time started: {datetime.now()}")
    print(f"Protocol: {protocol.upper()}")
    print(f"Number of threads: {num_threads}")
    if rate_limit:
        print(f"Rate limit: {rate_limit} seconds")
    print("-" * 50 + RESET)

    # Initialize a set to keep track of scanned ports
    scanned_ports = set()

    # Create threads for port scanning
    threads = []
    for _ in range(num_threads):
        for port in ports:
            thread = threading.Thread(target=scan_port, args=(target, port, protocol, scanned_ports, output_file, rate_limit))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Function to run the port scanner in interactive mode
def interactive_mode():
    print("Welcome to the ratScan Port Scanner!")
    target = input("Enter target IP address: ")
    protocol = input("Choose protocol (TCP/UDP): ").lower()
    while protocol not in ['tcp', 'udp']:
        print("Invalid protocol. Please choose TCP or UDP.")
        protocol = input("Choose protocol (TCP/UDP): ").lower()
    ports = input("Enter ports to scan (comma-separated list or range, e.g., '80,443'): ")
    num_threads = int(input("Enter number of threads: "))
    output_file = input("Enter output file path (leave empty for console output): ")
    rate_limit = float(input("Enter rate limit in seconds (optional, enter 0 for no rate limit): "))
    if not output_file:
        output_file = None

    # Parse ports
    ports = parse_ports(ports)

    # Perform port scanning
    scan_ports(target, ports, protocol, num_threads, output_file, rate_limit)

# Function to parse ports specified as a comma-separated list or range
def parse_ports(ports_str):
    ports = []
    for part in ports_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

# Main function
def main():
    parser = argparse.ArgumentParser(description="ratScan Port Scanner - Scan open ports on a target machine.")
    parser.add_argument("-i", "--interactive", action="store_true", help="run in interactive mode")
    parser.add_argument("-t", "--target", help="target IP address")
    parser.add_argument("-p", "--ports", help="ports to scan (comma-separated list or range, e.g., '80,443')")
    parser.add_argument("-n", "--threads", type=int, help="number of threads for concurrent scanning")
    parser.add_argument("-o", "--output", help="output file to save results")
    parser.add_argument("-r", "--rate-limit", type=float, help="rate limit in seconds (optional)")
    parser.add_argument("-u", "--protocol", choices=['tcp', 'udp'], help="protocol to use for scanning (TCP/UDP)")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.target and args.ports and args.threads and args.protocol:
        target = args.target
        ports = parse_ports(args.ports)
        protocol = args.protocol.lower()
        num_threads = args.threads
        output_file = args.output
        rate_limit = args.rate_limit if args.rate_limit else 0

        scan_ports(target, ports, protocol, num_threads, output_file, rate_limit)
    else:
        parser.print_help()

# Entry point
if __name__ == "__main__":
    main()
