import socket

# Server configuration
server_port = 12345

# Create a datagram socket with port address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', server_port))

print("Server is listening on port", server_port)

while True:
    # Receive datagram packets from the client
    data, client_address = server_socket.recvfrom(1024)
    print("Received data from client:", data.decode('utf-8'))

    # Send datagram packets to the client
    server_socket.sendto("Hello, client! This is the server.".encode('utf-8'), client_address)

# Close the socket (This part is reached only if the server is terminated)
server_socket.close()
