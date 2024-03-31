```
()-()   
 \"/ 
  `
```

# Interactive Port Scanner
The Interactive Port Scanner is a Python script that allows users to scan open ports on a target machine. It provides both interactive and non-interactive modes for flexibility.

## Features
* Interactive Mode: Users can interactively input target IP address, ports to scan, protocol, number of threads, output file path, and rate limit.
* Non-interactive Mode: Users can provide command-line arguments to specify target IP address, ports to scan, number of threads, output file path, and rate limit.
* Threading: Utilizes threading for concurrent port scanning, improving speed and efficiency.
* Output Saving: Option to save scan results to a file.
* Colorized Output: Color-coded output to easily identify open ports.
* Protocol Support: Supports both TCP and UDP protocols.
* Port Range Support: Allows scanning of port ranges or comma seperated list

## Usage
**Help**
* -h, --help menu
```
python3 ratScan.py -h
```

**Interactive Mode**
Run the script with -i:
```
python3 ratScan.py -i
```

**Non-interactive Mode**
Provide command-line arguments to specify target, ports, number of threads, protocol, output file, and rate limit:
```
python3 ratScan.py -t <target> -p <ports> -n <num_threads> -o <output_file> -r <rate_limit> -u <protocol>
```
**Command-line Arguments**
* -t, --target: Specify target IP addresses (comma-separated list).
* -p, --ports: Ports to scan (comma-separated list or range, e.g., '1-100').
* -n, --threads: Number of threads for concurrent scanning.
* -o, --output: Output file to save results (optional).
* -r, --rate-limit: Rate limit in seconds (optional).
* -u, --protocol: TCP/UDP
* -h, --help menu

## Requirements
* Python 3.x

## Example
Scan ports 1-100 on target IP address 192.168.1.100 using TCP protocol with 10 threads, saving results to output.txt, and a rate limit of 0.1 seconds:

```
python3 ratScan.py -t 192.168.1.1,192.168.1.2 -p 80,443 -n 10 -o scan_results.txt -r 0 -u tcp
```






