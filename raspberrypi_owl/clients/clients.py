import zmq


def main():
    # ZeroMQ Context
    context = zmq.Context()
    # Define the socket using the "Request" pattern
    socket = context.socket(zmq.REQ)
    # Replace <SERVER_IP> with the server's IP address
    socket.connect("tcp://<SERVER_IP>:5555")

    print("Client connected to server. Ready to send commands...")

    while True:
        # Get command from user input
        command = input(
            "Enter command (e.g., 'UPDATE_INI', 'UPLOAD_MODEL', 'CHANGE_CONFIG_FILE') "
            "or 'exit' to quit: "
        )

        if command.lower() == 'exit':
            break

        # Send command to server
        socket.send_string(command)

        # Receive response from server
        response = socket.recv_string()
        print(f"Received response: {response}")


if __name__ == "__main__":
    main()
