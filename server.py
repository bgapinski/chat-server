import sys
import socket
import select

HOST = "0.0.0.0"
PORT = 8080

#TODO: Use a logger instead of print


class Server():
    """
    A simple chat server.
    """
    def __init__(self, host=HOST, port=PORT, backlog=4):
        self.addr = (host, port)
        self.sock = socket.socket()

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.setblocking(0)

        self.sock.bind(self.addr)
        self.sock.listen(backlog)

        self.readers = [self.sock]
        self.writers = []
        self.errors = [sys.stderr]

    def serve(self):
        msgs = []
        while True:
            rlist, wlist, xlist = select.select(self.readers,
                                                self.writers,
                                                self.errors)

            for r in rlist:
                if r is self.sock:
                    client, (client_ip, client_port) = self.sock.accept()
                    self.readers.append(client)
                    self.writers.append(client)

                    print("Client connected from {}".format(client_ip))
                else:
                    msg = self.receive_message(r)
                    if msg:
                        msgs.append(msg)
                        print(msg)

            msg = msgs.pop(0) if msgs else ""
            for w in wlist:
                w.send(msg.encode())

    def receive_message(self, r):
        msg = r.recv(10).decode()
        if msg == "":
            self.readers.remove(r)
            self.writers.remove(r)
            print("Client disconnected from {}".format(
                r.getsockname()[0]))
            return ""
        else:
            while not msg[-1] == "\r":
                msg += r.recv(10).decode()
            return msg


if __name__ == '__main__':
    print("Server running. Waiting for connections.")
    server = Server()
    server.serve()
    sys.exit()
