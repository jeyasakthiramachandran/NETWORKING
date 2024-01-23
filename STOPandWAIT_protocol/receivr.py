import socket
import pickle

class Receiver:
    def __init__(self):
        self.receiver = None
        self.connection = None
        self.out_socket = None
        self.in_socket = None
        self.ack = ""
        self.pkt = None
        self.seq = 0
        self.delay = 0

    def run(self):
        receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver.bind(('localhost', 1500))
        receiver.listen(10)

        connection, _ = receiver.accept()
        print("Connection established:")

        out_socket = connection.makefile('wb')
        in_socket = connection.makefile('rb')

        while True:
            try:
                pkt = pickle.load(in_socket)
                ack, data = pkt

                if data == "Terminate":
                    break

                print(f"\nMsg received: {data}")
                print(f"sending ack {ack}")
                pickle.dump(ack, out_socket)
                out_socket.flush()

                self.seq = 1 if self.seq == 0 else 0

            except Exception as e:
                print(e)

        in_socket.close()
        out_socket.close()
        connection.close()
        receiver.close()
        print("\nConnection Terminated.")

if __name__ == "__main__":
    receiver = Receiver()
    receiver.run()

