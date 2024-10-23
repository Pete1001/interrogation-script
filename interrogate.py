'''
 by Pete Link  -->> c-pete.link@charter.com
 Personal email:  thepetelink@yahoo.com

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
from fileinput import filename
import paramiko
from getpass import getpass
import time
import csv

out = ''

username = input("Please enter your username: ")
password = getpass()

def read_hosts_from_file(filename):
    with open(filename, 'r') as f:
        hosts = f.read().splitlines()
    return hosts

def read_commands_from_file(file):
    with open(file, 'r') as fi:
        commands = fi.read().splitlines()
    return commands

def connect_and_execute(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    ssh.close()
    return output

if __name__ == "__main__":
    hosts_file = "hosts.txt"
    commands_file = 'commands.txt'
 
    commands = read_commands_from_file(commands_file)

    hosts = read_hosts_from_file(hosts_file)

    for host in hosts:
        print(f"Connecting to host: {host}...")
        try:
            for command in commands:
                output = connect_and_execute(host, username, password, command)
                print(f'Executing command: {command}')
                print(f'{output} \n \n \n')
                time.sleep(2)
                out += "\n" + host + "\n" + command + "\n" + output + "\n" + "-------------------------------" + "\n" + "\n" + "\n" + "\n"

        except Exception as e:
            print(f"Error connecting to {host}: {e}")

time.sleep(.5)
filename = ''.join(hosts)
with open(filename, "w") as file:
    file.write(out)
