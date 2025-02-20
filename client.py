import zmq

# Setting up the ZeroMQ client
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def main():
    while True:
        print("\nChoose an option:")
        print("H: Calculate heart rate intensity")
        print("T: Get information on how to check your heart rate")
        print("C: Calculate target heart rate")
        print("Q: Quit")  # Option to quit the program

        option = input("Enter your choice (H/T/C/Q): ").strip().upper()

        if option == "H":
            age = input("Enter your age: ")
            heart_rate = input("Enter your heart rate: ")
            request = f"H {age} {heart_rate}"
        elif option == "C":
            age = input("Enter your age: ")
            request = f"C {age} xxx"
        elif option == "T":
            request = "T xxx xxx"
        elif option == "Q":
            print("Exiting the program.")
            break  # Exit the loop and quit the program
        else:
            print("Invalid option.")
            continue  # Go back to the options menu

        # Send request to the server
        socket.send_string(request)

        # Get the response from the server
        message = socket.recv_string()
        print(f"{message}")

if __name__ == "__main__":
    main()