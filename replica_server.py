# replica_server.py
import socket
import sys
import random
import threading

HOST = "127.0.0.1"

def handle_client(conn, addr, replica_id, state):
    """
    Handle a single client connection.
    state is a dict so we can mutate a shared counter: state["counter"].
    """
    try:
        data = conn.recv(1024)
        if not data:
            return

        message = data.decode().strip()
        print(f"[Replica {replica_id}] Received from {addr}: {message}")

        # Simulate a random crash fault with probability p
        p_crash = 0.3
        if random.random() < p_crash:
            print(f"[Replica {replica_id}] Simulating crash! (process will exit)")
            # Flush output then exit process to simulate a crash
            conn.close()
            # In a real system you don't call exit here; this is just to see the effect.
            sys.exit(1)

        # Otherwise, process the request
        if message == "GET_COUNTER":
            state["counter"] += 1
            response = f"OK {state['counter']}\n"
        else:
            response = "ERROR unknown command\n"

        conn.sendall(response.encode())
        print(f"[Replica {replica_id}] Replied with: {response.strip()}")

    finally:
        conn.close()


def run_server(port, replica_id):
    state = {"counter": 0}  # shared state for this replica
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen()
        print(f"[Replica {replica_id}] Listening on {HOST}:{port}")

        while True:
            conn, addr = s.accept()
            # Handle each client in a thread for simplicity
            t = threading.Thread(
                target=handle_client,
                args=(conn, addr, replica_id, state),
                daemon=True
            )
            t.start()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python replica_server.py <port> <replica_id>")
        sys.exit(1)

    port = int(sys.argv[1])
    replica_id = sys.argv[2]
    run_server(port, replica_id)
