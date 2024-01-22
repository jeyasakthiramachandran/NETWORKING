import socket
import platform

# Server configuration
server_address = ('localhost', 12345)

# Create a client socket and connect to the server's port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    # Retrieve its own IP address using built-in function
    client_address = socket.gethostbyname(socket.gethostname())
    print("Client's IP Address:", client_address)

    # Send its address to the server
    client_socket.sendall(client_address.encode('utf-8'))

    # Display the date & time sent by the server
    server_time = client_socket.recv(1024).decode('utf-8')
    print("Server's Date & Time:", server_time)

except Exception as e:
    print("Error:", e)

finally:
    # Close the client socket
    client_socket.close()