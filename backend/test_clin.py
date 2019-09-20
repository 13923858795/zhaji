import socket, time

client = socket.socket()

client.connect(('localhost', 5859))


# client.send(cmd.encode())
cmd_res = client.recv(1024)
cmd_res2 = client.recv(1024)
print(cmd_res, cmd_res2)







