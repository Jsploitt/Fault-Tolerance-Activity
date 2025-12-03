# client.py
import socket
import time

REPLICAS = [
    ("127.0.0.1", 5000),
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002),
]

REQUEST_TIMEOUT = 1.0  # seconds


def send_request_to_replica(replica, message):
    host, port = replica
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(REQUEST_TIMEOUT)
        s.connect((host, port))
        s.sendall((message + "\n").encode())
        data = s.recv(1024)
        return data.decode().strip()


def send_request_with_retries(message, max_retries=3):
    """
    Try to send a request to any available replica.
    Retries across replicas, not to the same one.
    """
    attempt = 0
    last_error = None

    for _ in range(max_retries):
        for replica in REPLICAS:
            attempt += 1
            host, port = replica
            print(f"[Client] Attempt {attempt}: trying replica {host}:{port}")

            try:
                reply = send_request_to_replica(replica, message)
                print(f"[Client] Success from {host}:{port} -> {reply}")
                return reply
            except (socket.timeout, ConnectionRefusedError, OSError) as e:
                # timeout, connection refused, or crash mid-flight
                print(f"[Client] Failed with {host}:{port}: {e}")
                last_error = e

        # Optional small delay between cycles over all replicas
        time.sleep(0.2)

    raise RuntimeError(f"All replicas failed after {attempt} attempts. Last error: {last_error}")


if __name__ == "__main__":
    # Send a few requests to see fault tolerance in action
    for i in range(1, 6):
        print(f"\n[Client] === Request {i} ===")
        try:
            reply = send_request_with_retries("GET_COUNTER")
            print(f"[Client] Final reply: {reply}")
        except RuntimeError as e:
            print(f"[Client] Request {i} failed: {e}")
        time.sleep(0.5)
