import socket
import pickle

class SlideSender:
    def __init__(self):
        self.sender = None
        self.out_socket = None
        self.in_socket = None
        self.pkt = None
        self.data = 'a'
        self.SeqNum = 1
        self.SWS = 5
        self.LAR = 0
        self.LFS = 0
        self.NF = 0

    def send_frames(self):
        if self.SeqNum <= 15 and self.SWS > (self.LFS - self.LAR):
            try:
                self.NF = self.SWS - (self.LFS - self.LAR)
                for _ in range(self.NF):
                    self.pkt = f"{self.SeqNum} {self.data}"
                    self.sender.send(pickle.dumps(self.pkt))
                    self.LFS = self.SeqNum
                    print(f"Sent {self.SeqNum} {self.data}")

                    self.data = chr((ord(self.data) - ord('a') + 1) % 6 + ord('a'))
                    self.SeqNum += 1
            except Exception as e:
                print(e)

    def run(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender.connect(('localhost', 1500))

        while self.LAR < 15:
            try:
                self.send_frames()

                ack = int(pickle.loads(self.sender.recv(1024)))
                self.LAR = ack
                print(f"ack received: {ack}")
            except Exception as e:
                print(e)

        self.sender.close()
        print("\nConnection Terminated.")

if __name__ == "__main__":
    sender = SlideSender()
    sender.run()
