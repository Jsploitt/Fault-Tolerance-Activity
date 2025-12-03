# async_replica_server.py
import asyncio
import random
import sys

HOST = "127.0.0.1"


async def handle_client(reader: asyncio.StreamReader,
                        writer: asyncio.StreamWriter,
                        replica_id: str,
                        state: dict):
    addr = writer.get_extra_info("peername")
    try:
        data = await reader.readline()
        if not data:
            writer.close()
            await writer.wait_closed()
            return

        message = data.decode().strip()
        print(f"[Replica {replica_id}] Received from {addr}: {message}")

        # Simulate a random crash fault with probability p
        p_crash = 0.3
        if random.random() < p_crash:
            print(f"[Replica {replica_id}] Simulating crash! (process will exit)")
            writer.close()
            await writer.wait_closed()
            # Kill this server process to simulate a crash
            sys.exit(1)

        # Normal processing
        if message == "GET_COUNTER":
            state["counter"] += 1
            response = f"OK {state['counter']}\n"
        else:
            response = "ERROR unknown command\n"

        writer.write(response.encode())
        await writer.drain()
        print(f"[Replica {replica_id}] Replied with: {response.strip()}")

    except Exception as e:
        print(f"[Replica {replica_id}] Error handling {addr}: {e!r}")
    finally:
        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()


async def main(port: int, replica_id: str):
    state = {"counter": 0}

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, replica_id, state),
        HOST,
        port,
    )

    addr = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[Replica {replica_id}] Listening on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python async_replica_server.py <port> <replica_id>")
        sys.exit(1)

    port = int(sys.argv[1])
    replica_id = sys.argv[2]

    try:
        asyncio.run(main(port, replica_id))
    except KeyboardInterrupt:
        print(f"[Replica {replica_id}] Shutting down...")
