import logging
import socket
import argparse
import struct
from pathlib import Path

log_level: int = logging.DEBUG

if __name__ == "__main__":
    print("> Starting server")

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
    parser.add_argument("--output", type=Path, required=True)

    # Read args
    args = parser.parse_args()
    HOST = args.host
    PORT = args.port
    TOUT = args.timeout
    o_dir = args.output

    # Listen for incoming connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        # Only one client is served
        server.listen(1)
        server.settimeout(TOUT)

        logging.info("Listening on %s:%d ...", HOST, PORT)

        try:
            connection, address = server.accept()
        except TimeoutError:
            # No connection established. Exiting
            logging.warning("No client appeared within %d seconds", TOUT)
        else:
            # Succesful connection
            with connection:
                logging.info("Connected with %s", address)

                # Receive data from client, if available and extract file name
                o_file_name_len = struct.unpack("!I", connection.recv(4))[0]
                if o_file_name_len:
                    o_file_name = connection.recv(o_file_name_len).decode(UTF8)
                    logging.info("Received %s from client", o_file_name)

                    # Create File path
                    o_dir.mkdir(exist_ok=True)
                    o_file = o_dir / Path(o_file_name)

                    # Check if file already exists
                    if o_file.exists():
                        # Don't ovveride it
                        logging.info(
                                "File %s already exists. Won't ovveride",
                                o_file
                        )
                        while connection.recv(1024):
                            # Avoid abrupting connection by draining client
                            pass
                    else:
                        # Store transmitted file
                        with o_file.open("wb") as file:
                            # Read file to end of transmission
                            while True:
                                data = connection.recv(1024)
                                if not data:
                                    break
                                file.write(data)

    print("> Shutting down")
