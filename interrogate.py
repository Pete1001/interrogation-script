'''
# interrogate.py
#
# Author:      Pete Link
# Date:        October 2024
# Description: Script to gather command outputs from network switches using SSH.

## Contact
For questions or suggestions, feel free to open an issue or contact me via [GitHub](https://github.com/Pete1001).

 Use:        python3 `filename`
 Tested on:  enwdcocd01n

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
    -please note that by default, the script inserts 'term len 0','show run | i hostsname','show ver', and 'show clock' as the first commands
    
    commands.txt example:
    
        show int desc | in up
        sho ip int bri | i up
        sh cdp nei
        sh run
'''
import paramiko
from getpass import getpass
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# Setting up logging to log the session interactively with clear separators
logging.basicConfig(filename='session.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# User input for username and password
username = input("Please enter your username: ")
password = getpass()

# Read hosts and commands from files
def read_hosts_from_file(filename):
    with open(filename, 'r') as f:
        hosts = f.read().splitlines()
    return hosts

def read_commands_from_file(file):
    with open(file, 'r') as fi:
        commands = fi.read().splitlines()
    return commands

# Function to retry a task in case of failure
def retry(func, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    logging.error(f"All retries failed")
    return None

# Establish an SSH connection and execute multiple commands persistently
def connect_and_execute_persistent(host, username, password, commands):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, timeout=10)

        logging.info(f"Connected to: {host}")
        
        shell = ssh.invoke_shell()
        time.sleep(1)  # Allow some time to establish the session
        
        output = ""
        for command in commands:
            shell.send(command + '\n')
            time.sleep(2)  # Give time for the command to execute
            command_output = ""
            while shell.recv_ready():
                command_output += shell.recv(1024).decode('utf-8')

            # Add clear separation for each command in the output file
            output += f"\n{'-'*40}\nCommand: {command}\n{'-'*40}\n{command_output.strip()}\n"
            logging.info(f"Executed command on {host}: {command}")
        
        ssh.close()
        return output.strip()  # Clean output by removing excessive whitespace
    except Exception as e:
        logging.error(f"Error connecting to {host}: {e}")
        return None

# Run the process for each host
def run_on_host(host):
    output_file = f"{host}_output.txt"
    with open(output_file, "w") as file:
        commands = read_commands_from_file(commands_file)
        
        # Add a header to indicate start of output for this host
        file.write(f"\n{'='*40}\nOutput for host: {host}\n{'='*40}\n")
        logging.info(f"Starting session for host: {host}\n{'='*40}")
        
        try:
            output = retry(lambda: connect_and_execute_persistent(host, username, password, commands))
            if output:
                logging.info(f'Commands executed on {host}')
                file.write(f"{output}\n")
                file.write(f"\n{'='*40}\nEnd of output for host: {host}\n{'='*40}\n")
            else:
                file.write(f"Failed to execute commands on {host}\n{'='*40}\n")
        except Exception as e:
            logging.error(f"Error during session with {host}: {e}")
            file.write(f"Error during session with {host}: {e}\n{'='*40}\n")

if __name__ == "__main__":
    hosts_file = "hosts.txt"
    commands_file = 'commands.txt'

    # Read hosts and commands
    hosts = read_hosts_from_file(hosts_file)

    # Parallel execution of hosts with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_on_host, hosts)

    logging.info("All tasks completed.")
