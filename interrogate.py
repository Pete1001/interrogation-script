'''
# interrogate.py
#
# Author:      Pete Link
# Date:        October 2024
# Description: Script to gather command outputs from network devices using SSH.

## Contact
For questions or suggestions, feel free to open an issue or contact me via [GitHub](https://github.com/Pete1001).

 Use:        python3 `filename`

 Current directory must containt the following files:
    -hosts.txt
    -commands.txt
    
hosts.txt must be named "hosts.txt".  The file must be located in the current directory and must be formatted in the following way:
    -one hostname or IP Address per line with no commas, quotes or spaces.
    
    -hosts.txt example:

        92.168.0.1
        192.168.0.2

commands.txt must be named "commands.txt".  The file must be located in the current directory and must be formatted in the following way:
    -one command per line with no commas, quotes or spaces
    -simply type it exactly as you would at the command line
    
    commands.txt example:
    
        show int desc | in up
        sho ip int bri | i up
        sh cdp nei
        sh run

base_commands.txt can contain commands that can be executed first on any device.  These commands are simply helper commands.
The file must be located in the current directory and must be formatted in the following way:
    -one command per line with no commas, quotes or spaces
    -simply type it exactly as you would at the command line

    base_commands.txt example:

        term len 0
        show run | i hostname
        show clock

'''
import paramiko
from getpass import getpass
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# Function to set up a logger for each host
def setup_logger(host):
    logger = logging.getLogger(host)
    logger.setLevel(logging.INFO)
    
    # Create a file handler for the specific host
    handler = logging.FileHandler(f"{host}_session.log") #if desired; mode = 'w' overwrites the log file each time the script is run for each host
    handler.setLevel(logging.INFO)
    
    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)
    
    return logger

# User input for username and password
username = input("Please enter your username: ")
password = getpass()

# Read hosts, base commands, and commands from files
def read_hosts_from_file(filename):
    with open(filename, 'r') as f:
        hosts = f.read().splitlines()
    return hosts

def read_commands_from_file(file):
    with open(file, 'r') as fi:
        commands = fi.read().splitlines()
    return commands

# Function to retry a task in case of failure
def retry(func, logger, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    logger.error(f"All retries failed")
    return None

# Establish an SSH connection and execute multiple commands persistently
def connect_and_execute_persistent(host, username, password, commands, logger):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, timeout=10)

        # Print to console when connecting to a host
        print(f"Connecting to {host}...")

        logger.info(f"Connected to {host}")
        logger.info(f"{'='*10} Starting session for host: {host} {'='*10}")
        
        shell = ssh.invoke_shell()
        time.sleep(3)  # Allow some time to establish the session
        
        output = ""
        for command in commands:
            # Print to console when running a command on a host
            print(f"Executing command on {host}: {command}")
            
            logger.info(f"{'-'*10} Executing command: {command} {'-'*10}")
            shell.send(command + '\n')
            time.sleep(5)  # Give time for the command to execute
            
            command_output = ""
            while shell.recv_ready():
                command_output += shell.recv(1024).decode('utf-8')

            # Log truncated output to avoid clutter in the log file
            truncated_output = command_output.strip()[:200] + '...' if len(command_output.strip()) > 200 else command_output.strip()
            logger.debug(f"Command output (truncated): {truncated_output}")
            
            # Add separation for each command in the output file
            output += f"\n{'-'*10}\nCommand: {command}\n{'-'*10}\n{command_output.strip()}\n"
        
        ssh.close()
        logger.info(f"{'='*10} Finished session for host: {host} {'='*10}")
        
        # Print to console when done with a host
        print(f"Finished session for {host}")
        return output.strip()  # Clean output by removing excessive whitespace
    except Exception as e:
        logger.error(f"Error connecting to {host}: {e}")
        print(f"Error connecting to {host}")
        return None

# Run the process for each host
def run_on_host(host):
    output_file = f"{host}_output.txt"
    with open(output_file, "w") as file:
        
        # Read base commands first, then regular commands, and combine them
        base_commands = read_commands_from_file(base_commands_file)
        custom_commands = read_commands_from_file(commands_file)
        commands = base_commands + custom_commands  # Combine the commands (base first)
        
        # Set up a separate logger for each host
        logger = setup_logger(host)
        
        # Add a header to indicate start of output for this host
        file.write(f"\n{'='*10}\nOutput for host: {host}\n{'='*10}\n")
        logger.info(f"Starting session for host: {host}\n{'='*10}")
        
        try:
            output = retry(lambda: connect_and_execute_persistent(host, username, password, commands, logger), logger)
            if output:
                logger.info(f"Commands executed successfully on {host}")
                file.write(f"{output}\n")
                file.write(f"\n{'='*10}\nEnd of output for host: {host}\n{'='*10}\n")
            else:
                file.write(f"Failed to execute commands on {host}\n{'='*10}\n")
        except Exception as e:
            logger.error(f"Error during session with {host}: {e}")
            file.write(f"Error during session with {host}: {e}\n{'='*10}\n")

if __name__ == "__main__":
    hosts_file = "hosts.txt"
    base_commands_file = 'base_commands.txt'  # Base commands file to read first
    commands_file = 'commands.txt'

    # Read hosts and commands
    hosts = read_hosts_from_file(hosts_file)

    # Parallel execution of hosts with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_on_host, hosts)

    print("All tasks completed.  Have a nice day!")
