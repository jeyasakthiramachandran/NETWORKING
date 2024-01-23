import socket
import pickle

class Sender:
    def __init__(self):
        self.sender = None
        self.out_socket = None
        self.in_socket = None
        self.pkt = None
        self.ack = ""
        self.data = ""
        self.seq = 0
        self.dup = False

    def run(self):
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect(('localhost', 1500))
        sender.settimeout(5)

        out_socket = sender.makefile('wb')
        in_socket = sender.makefile('rb')

        while True:
            try:
                if self.dup:
                    pickle.dump((self.seq, self.data), out_socket)
                    out_socket.flush()
                    self.dup = False
                else:
                    data = input("\nEnter the data to send ('Terminate' to end): ").strip()
                    self.pkt = (self.seq, data)
                    pickle.dump(self.pkt, out_socket)
                    out_socket.flush()

                try:
                    ack = pickle.load(in_socket)

                    if data == "Terminate":
                        break

                    if ack == self.seq:
                        print(f"ack received: {ack}")
                        self.seq = 1 if self.seq == 0 else 0
                    else:
                        self.dup = True

                except socket.timeout:
                    print("Ack timeout. Resend data")
                    self.dup = True

            except Exception as e:
                print(e)

        in_socket.close()
        out_socket.close()
        sender.close()
        print("\nConnection Terminated.")

if __name__ == "__main__":
    sender = Sender()
    sender.run()
