# Network Devices Interrogation Collector

This Python script automates gathering command outputs from network devices by connecting via SSH. It reads hosts (devices IPs or hostnames) and commands from external files (`hosts.txt`, `base_commands.txt`, and `commands.txt`), and outputs the results for each host into a separate file. The script also logs the entire session interactively for each host.

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
- **Automated SSH connection**: Establishes secure connections to multiple network devices using SSH.
- **Command execution**: Executes multiple commands on each device as specified in the input file.
- **Base commands execution**: Executes a predefined set of base commands (from `base_commands.txt`) before any custom commands from `commands.txt`.
- **Parallel processing**: Executes commands on multiple devices concurrently to save time.
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
   git clone https://github.com/Pete1001/interrogation-script.git
   ```

2. **Navigate to the directory**:
   ```bash
   cd interrogation-script
   ```

3. **Ensure `hosts.txt`, `base_commands.txt`, and `commands.txt` files are present** in the same directory (See below for the required format).

## Usage

### Input Files

#### `hosts.txt`
The `hosts.txt` file should contain a list of network device IP addresses or hostnames. Each line should contain one host, with no commas or additional characters.

Example:
```
192.168.0.1
192.168.0.2
10.0.0.5
```
FUTURE DEVELOPMENT:  (Notes for Pete)
   -Write some decent output to the CONSOLE!!!
   -Each run of the scripts - overwrite all the output logs
   -Add functionality for Mandatory General System Health Check
   -Add functionality for Manual Diff Pre/Post Checks
      -Run Pre and Post and write each to a separate file for each host
      -Do a diff between these files and write the output of the diff

#### `base_commands.txt`
The `base_commands.txt` file should contain a list of base commands that will be executed **first** on every device. These are usually commands that set terminal behavior or gather specific information common to all devices.

Example:
```
term len 0
show run | include hostname
show clock
```

#### `commands.txt`
The `commands.txt` file should contain a list of commands that you want to execute after the base commands. Each line should be a command as you would type it on the device's command line.

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
   python3 interrogation.py
   ```

2. The script will:
   - Read from `hosts.txt`, `base_commands.txt`, and `commands.txt`.
   - Combine the base commands from `base_commands.txt` with the custom commands from `commands.txt` (base commands will be executed first).
   - Connect to each host (network device) via SSH.
   - Execute the combined list of commands on each host.
   - Save the output in individual files named `{host}_output.txt`.

### Example Interaction

```bash
$ python3 interrogation.py
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
Command: term len 0
----------------------------------------
<Command output here>
----------------------------------------
Command: show version
----------------------------------------
<Command output here>
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
2024-10-23 10:00:10 - INFO - ---------------------------------------- Executing command: term len 0 ----------------------------------------
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
  - Ensure that the network devices are reachable (e.g., via `ping`).
  - Verify that the SSH service is enabled on the devices.
  - Double-check the credentials being entered.
  
- **Command Errors**:
  If specific commands fail, it may be due to the privilege level or syntax issues. Ensure that the user has sufficient privileges to execute the commands on the device.

- **Logging**:
  Review the individual `{host}_session.log` files for detailed error messages or connection issues.

## Contributing

We welcome contributions to enhance the script, including new features, bug fixes, and optimizations. If you'd like to contribute, please fork the repository and submit a pull request.

## License

MIT License
Copyright (c) 2024 [Pete Link]
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
