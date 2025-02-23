import sys

def print_message(message):
    print(f"Received message: {message}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        print_message(message)
    else:
        print("No message provided")
