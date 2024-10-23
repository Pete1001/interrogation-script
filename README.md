
# Network Switch Output Collector

This Python script automates gathering command outputs from network switches by connecting via SSH. It reads hosts (switch IPs or hostnames) and commands from external files (`hosts.txt` and `commands.txt`), and outputs the results for each host into a separate file. The script also logs the entire session interactively for review, with improvements to logging such that each host has its own session log file.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Input Files](#input-files)
   - [Running the Script](#running-the-script)
5. [Output Format](#output-format)
6. [Logging](#logging)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

## Features
- **Automated SSH connection**: Establishes secure connections to multiple network switches using SSH.
- **Command execution**: Executes multiple commands on each switch as specified in the input file.
- **Parallel processing**: Executes commands on multiple switches concurrently to save time.
- **Output separation**: Clear separation between outputs for each host using `=` signs, and between commands using `-` signs.
- **Session logging per host**: Logs for each host are saved in separate log files for easier management.

## Prerequisites
Before using this script, ensure you have the following:
- **Python 3.6+**
- **paramiko**: A Python library for handling SSH connections.

You can install the necessary packages using pip:

```bash
pip install paramiko
```

## Installation

1. **Clone the repository** (or copy the script to your machine):
   ```bash
   git clone https://github.com/your-repo/network-switch-output-collector.git
   ```

2. **Navigate to the directory**:
   ```bash
   cd network-switch-output-collector
   ```

3. **Ensure `hosts.txt` and `commands.txt` files are present** in the same directory (See below for the required format).

## Usage

### Input Files

#### `hosts.txt`
The `hosts.txt` file should contain a list of network switch IP addresses or hostnames. Each line should contain one host, with no commas or additional characters.

Example:
```
192.168.0.1
192.168.0.2
10.0.0.5
```

#### `commands.txt`
The `commands.txt` file should contain a list of commands that you want to execute on each switch. Each line should be a command as you would type it on the switch's command line.

Example:
```
show version
show interfaces
show ip route
```

### Running the Script

1. **Run the script** using Python. It will prompt you to enter your SSH username and password.

   Example:
   ```bash
   python3 network_switch_collector.py
   ```

2. The script will:
   - Read from `hosts.txt` and `commands.txt`.
   - Connect to each host (network switch) via SSH.
   - Execute the commands specified in `commands.txt` on each host.
   - Save the output in individual files named `{host}_output.txt`.

### Example Interaction

```bash
$ python3 network_switch_collector.py
Please enter your username: admin
Password: **********
```

### Output Format

The output for each host will be saved in a file named `{host}_output.txt`. Each host's outputs are separated by lines of `=` signs, and each command's output is separated by lines of `-` signs for clarity.

#### Example Output for a Host (`192.168.0.1_output.txt`):

```text
========================================
Output for host: 192.168.0.1
========================================
----------------------------------------
Command: show version
----------------------------------------
Cisco IOS XE Software, Version 16.12.1
...
----------------------------------------
Command: show interfaces
----------------------------------------
GigabitEthernet0/0 is up
...
========================================
End of output for host: 192.168.0.1
========================================
```

### Logging

Each session's activity is now logged in a **separate log file for each host**. The log file is named `{host}_session.log`.

These log files include:
- Connection attempts to each host.
- Commands executed on each host.
- Any errors or exceptions encountered during execution.

#### Example Log Output (`192.168.0.1_session.log`):

```text
2024-10-23 10:00:00 - INFO - Connected to 192.168.0.1
2024-10-23 10:00:05 - INFO - ======================================== Starting session for host: 192.168.0.1 ========================================
2024-10-23 10:00:10 - INFO - ---------------------------------------- Executing command: show version ----------------------------------------
2024-10-23 10:00:12 - DEBUG - Command output (truncated): Cisco IOS XE Software, Version 16.12.1, RELEASE SOFTWARE (fc3)...
2024-10-23 10:00:15 - INFO - ======================================== Finished session for host: 192.168.0.1 ========================================
```

### Parallel Execution

The script uses Python's `ThreadPoolExecutor` to execute commands on multiple hosts concurrently. The number of parallel threads can be configured in the script by adjusting the `max_workers` parameter in the `ThreadPoolExecutor`.

```python
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_on_host, hosts)
```

This ensures that commands are executed on up to 5 hosts at the same time.

### Troubleshooting

- **Connection Errors**:
  If you encounter connection issues, check the following:
  - Ensure that the network switches are reachable (e.g., via `ping`).
  - Verify that the SSH service is enabled on the switches.
  - Double-check the credentials being entered.
  
- **Command Errors**:
  If specific commands fail, it may be due to the privilege level or syntax issues. Ensure that the user has sufficient privileges to execute the commands on the switch.

- **Logging**:
  Review the individual `{host}_session.log` files for detailed error messages or connection issues.

## Contributing

We welcome contributions to enhance the script, including new features, bug fixes, and optimizations. If you'd like to contribute, please fork the repository and submit a pull request.

## License

MIT License
Copyright (c) 2024 [Pete Link]
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
