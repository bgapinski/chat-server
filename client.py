import socket
import select
import sys

IP = "localhost"
PORT = 8080


class Client():
    """
    A simple chat client.
    """
    def __init__(self, host=IP, port=PORT):
        self.remote = (host, port)
        self.server = socket.socket()

        self.readers = [self.server, sys.stdin]
        self.writers = [self.server]
        self.errors = [sys.stderr]

        print("Connecting to server...")
        try:
            self.server.connect(self.remote)
        #except ConnectionRefusedError:
        except:
            print("Connection was refused :(")
            sys.exit(1)
        else:
            print("Connection successful!")
            self.chat()

    def chat(self):
        m = ''
        print(">> ", end="", flush=True)
        while True:
            rlist, wlist, xlist = select.select(self.readers,
                                                self.writers,
                                                self.errors)

            for r in rlist:
                if r is sys.stdin:
                    m += sys.stdin.readline().rstrip("\n")
                else:
                    msg = r.recv(10)
                    print(msg.decode())
                    print(">> ", end="", flush=True)

            for w in wlist:
                if m:
                    w.sendall(m.encode())
                    m = ''


if __name__ == '__main__':
    client = Client()
