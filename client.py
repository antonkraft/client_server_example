import logging
import socket
import argparse
from pathlib import Path
import struct
from tqdm import tqdm

log_level: int = logging.DEBUG

if __name__ == "__main__":
    print("> Starting client")

    # Default values
    HOST = "127.0.0.1"
    PORT = 8001
    TOUT = 5
    UTF8 = "utf-8"

    # Setup logger
    logging.basicConfig(
            level=log_level,
            format="> %(asctime)s %(levelname)s: %(message)s"
    )

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=False, default=HOST)
    parser.add_argument("--port", type=int, required=False, default=PORT)
    parser.add_argument("--timeout", type=int, required=False, default=TOUT)
    parser.add_argument("--input", type=Path, required=True)

    # Read args
    args = parser.parse_args()
    HOST = args.host
    PORT = args.port
    TOUT = args.timeout
    i_file = args.input

    # Attempting connection to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        client.settimeout(TOUT)

        # Data for transfer
        i_file_name = i_file.name.encode(UTF8)
        logging.debug("Opened %s", i_file_name)

        try:
            logging.info("Connecting to %s:%d ...", HOST, PORT)
            client.connect((HOST, PORT))
        except (TimeoutError, ConnectionRefusedError):
            # Failed to connect
            logging.warning(
                    "Could not connect to server within %d seconds",
                    TOUT
            )
        else:
            # Succesful connection
            logging.info("Connected to server %s:%d", HOST, PORT)

            # Package and send content in 1KB chunks
            client.sendall(struct.pack("!I", len(i_file_name)))
            client.sendall(i_file_name)
            with i_file.open("rb") as file:
                with tqdm(
                        total=i_file.stat().st_size,
                        unit='B',
                        unit_scale=True,
                        desc=i_file_name.decode()
                ) as bar:
                    while chunk := file.read(1024):
                        client.sendall(chunk)
                        bar.update(len(chunk))

            # Signal end of transmission
            client.shutdown(socket.SHUT_WR)

    print("> Exiting")
