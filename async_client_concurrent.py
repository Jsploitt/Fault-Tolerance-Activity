# async_client.py
import asyncio
from typing import Tuple

REPLICAS = [
    ("127.0.0.1", 5000),
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002),
]

REQUEST_TIMEOUT = 0.5      # seconds
MAX_REPLICA_ROUNDS = 3     # how many times to cycle through replica list
TOTAL_REQUESTS = 50        # total logical requests we want to send
MAX_CONCURRENT = 10         # limit of in-flight requests

# Statistics tracking for Task 3
replica_success_counts = {
    ("127.0.0.1", 5000): 0,
    ("127.0.0.1", 5001): 0,
    ("127.0.0.1", 5002): 0,
}


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


async def send_request_with_retries(message: str, req_id: int) -> Tuple[str, tuple]:
    """
    Sends a request with retries and failover.
    Returns: (reply, replica_tuple) on success, raises RuntimeError on failure.
    """
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
                # Log which replica served this request
                print(f"Request {req_id} served by {host}:{port} with reply \"{reply}\"")
                return reply, replica
            except (asyncio.TimeoutError,
                    ConnectionRefusedError,
                    OSError,
                    ConnectionError) as e:
                print(f"[Client] Failed with {host}:{port}: {e}")
                last_error = e

        await asyncio.sleep(0.2)  # small pause before trying all replicas again

    raise RuntimeError(
        f"All replicas failed after {attempt} attempts. Last error: {last_error}"
    )


async def one_logical_request(req_id: int, sem: asyncio.Semaphore):
    """
    Represents one logical client request, protected by a semaphore to
    limit concurrent in-flight operations.
    """
    async with sem:
        print(f"\n[Client] === Logical Request {req_id} ===")
        try:
            reply, replica = await send_request_with_retries("GET_COUNTER", req_id)
            print(f"[Client] Logical Request {req_id} -> Final reply: {reply}")
            # Update replica statistics
            replica_success_counts[replica] += 1
            return True
        except RuntimeError as e:
            print(f"[Client] Logical Request {req_id} failed: {e}")
            return False


async def main():
    sem = asyncio.Semaphore(MAX_CONCURRENT)

    tasks = [
        asyncio.create_task(one_logical_request(i, sem))
        for i in range(1, TOTAL_REQUESTS + 1)
    ]

    # Wait for all logical requests to complete
    results = await asyncio.gather(*tasks)

    ok = sum(results)
    fail = len(results) - ok
    
    # Print per-replica statistics
    print("\n" + "="*50)
    print("PER-REPLICA STATISTICS")
    print("="*50)
    for replica, count in replica_success_counts.items():
        host, port = replica
        print(f"Replica {host}:{port} served {count} successful requests")
    
    print(f"\nTotal succeeded: {ok}, Total failed: {fail}")
    print("="*50)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[Client] Stopped by user.")
