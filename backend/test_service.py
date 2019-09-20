# import socket  # 导入 socket 模块
# import time
# s = socket.socket()  # 创建 socket 对象
# host = '0.0.0.0'  # 获取本地主机名
# port = 5858  # 设置端口
# s.bind((host, port))  # 绑定端口
#
# s.listen(5)  # 等待客户端连接
#
# now_time = time.time()
# ids = [i for i in range(0, 100)]
# comment = []
# for i in ids:
#     _c = f'CLR CARD {i}\r\n'.encode()
#     # comment.append(f'GET CARD {i}\r\n')
#
#     c, addr = s.accept()  # 建立客户端连接
#     print(_c)
#     c.send(_c)
#
#     a = c.recv(1024)
#     print(a)
#
#     c.close()



import socketserver
import time
config = {
    'SOCKET_HOST': '0.0.0.0',
    'SOCKET_PORT': 5859
}


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.request.settimeout(5)

    def handle(self):

            _c = f'CLR CARD 1\r\n'.encode()
            self.request.sendall(_c)

            _c = f'CLR CARD 2\r\n'.encode()
            self.request.sendall(_c)


            a = self.request.recv(1024)
            print(a)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":

            server = ThreadedTCPServer((config['SOCKET_HOST'], config['SOCKET_PORT']), ThreadedTCPRequestHandler)
            # print('starting server on {}:{}.'.format(config['SOCKET_HOST'], str(config['SOCKET_PORT'])))
            server.serve_forever()
