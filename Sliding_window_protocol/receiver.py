import socket
import pickle
import random

class SlideReceiver:
    def __init__(self):
        self.receiver = None
        self.conc = None
        self.out_socket = None
        self.in_socket = None
        self.ack = None
        self.pkt = None
        self.data = ''
        self.SeqNum = 0
        self.RWS = 5
        self.LFR = 0
        self.LAF = self.LFR + self.RWS
        self.delay = 0
        self.rand = random.Random()

    def run(self):
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind(('localhost', 1500))
        self.receiver.listen(1)
        self.conc, _ = self.receiver.accept()

        if self.conc:
            print("Connection established:")

        self.out_socket = self.conc.makefile('wb')
        self.in_socket = self.conc.makefile('rb')

        while self.LFR < 15:
            try:
                self.pkt = pickle.loads(self.in_socket.readline())
                ack, self.data = self.pkt.split()
                self.LFR = int(ack)

                if self.SeqNum <= self.LFR or self.SeqNum > self.LAF:
                    print(f"\nMsg received: {self.data}")
                    self.delay = self.rand.randint(0, 4)

                    if self.delay < 3 or self.LFR == 15:
                        self.out_socket.write(f"{ack}\n".encode('utf-8'))
                        self.out_socket.flush()
                        print(f"sending ack {ack}")
                        self.SeqNum += 1
                    else:
                        print("Not sending ack")
                else:
                    self.out_socket.write(f"{self.LFR}\n".encode('utf-8'))
                    self.out_socket.flush()
                    print(f"resending ack {self.LFR}")
            except Exception as e:
                print(e)

        self.in_socket.close()
        self.out_socket.close()
        self.receiver.close()
        print("\nConnection Terminated.")

if __name__ == "__main__":
    receiver = SlideReceiver()
    receiver.run()
