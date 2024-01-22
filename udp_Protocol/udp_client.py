import socket

# Server configuration
server_address = ('localhost', 12345)

# Create a datagram socket with server's IP address
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Create datagram packets with data
    data = "Hello, server! This is the client."

    # Send datagram packets to the server
    client_socket.sendto(data.encode('utf-8'), server_address)

    # Receive datagram packets from the server
    server_response, _ = client_socket.recvfrom(1024)
    print("Received data from server:", server_response.decode('utf-8'))

finally:
    # Close the socket
    client_socket.close()
