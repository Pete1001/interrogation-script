for ip in hosts:
    print(f'Connecting to host: {ip}')
    client.connect (ip, 22, user, password)
    commands = client.invoke_shell()

    for command in command_list:
        commands.send(f'{command} \n \n \n \n \n \n')
        time.sleep(2)
        output = commands.recv(1000000)
        output = output.decode("utf-8")
        #print(output)
        out += output
