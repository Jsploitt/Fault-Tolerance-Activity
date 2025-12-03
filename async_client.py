# async_client.py
import asyncio

REPLICAS = [
    ("127.0.0.1", 5000),
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002),
]

REQUEST_TIMEOUT = 1.0  # seconds
MAX_REPLICA_ROUNDS = 3  # how many times to cycle through replica list


async def send_request_to_replica(replica, message: str) -> str:
    host, port = replica
    reader, writer = await asyncio.open_connection(host, port)

    # Send request
    writer.write((message + "\n").encode())
    await writer.drain()

    # Wait for reply with timeout
    try:
        data = await asyncio.wait_for(reader.readline(), timeout=REQUEST_TIMEOUT)
    finally:
        writer.close()
        await writer.wait_closed()

    if not data:
        raise ConnectionError("Empty response from replica")

    return data.decode().strip()


async def send_request_with_retries(message: str) -> str:
    attempt = 0
    last_error = None

    for round_idx in range(MAX_REPLICA_ROUNDS):
        for replica in REPLICAS:
            attempt += 1
            host, port = replica
            print(f"[Client] Attempt {attempt}: trying replica {host}:{port}")

            try:
                reply = await send_request_to_replica(replica, message)
                print(f"[Client] Success from {host}:{port} -> {reply}")
                return reply
            except (asyncio.TimeoutError,
                    ConnectionRefusedError,
                    OSError,
                    ConnectionError) as e:
                print(f"[Client] Failed with {host}:{port}: {e}")
                last_error = e

        # Optional short pause before trying all replicas again
        await asyncio.sleep(0.2)

    raise RuntimeError(
        f"All replicas failed after {attempt} attempts. Last error: {last_error}"
    )


async def main():
    # Fire a few sequential requests
    for i in range(1, 6):
        print(f"\n[Client] === Request {i} ===")
        try:
            reply = await send_request_with_retries("GET_COUNTER")
            print(f"[Client] Final reply: {reply}")
        except RuntimeError as e:
            print(f"[Client] Request {i} failed: {e}")
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[Client] Stopped by user.")
