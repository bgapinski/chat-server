import socket
import select
import sys

IP = "localhost"
PORT = 8080

#TODO: Change all these prints into log messages


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
                    print(">> ", end="", flush=True)
                    m += sys.stdin.readline().rstrip("\n")
                else:
                    msg = self.receive_message(r)
                    if msg == "":
                        print("Connection closed by server.")
                        sys.exit(1)  # Should turn this into an exception

                    print(msg)

            for w in wlist:
                if m:
                    m += "\r"
                    w.send(m.encode())
                    m = ''

    def receive_message(self, r):
        msg = r.recv(10).decode()
        if msg == "":
            return ""
        else:
            while not msg[-1] == "\r":
                msg += r.recv(10).decode()
            return msg


if __name__ == '__main__':
    client = Client()
