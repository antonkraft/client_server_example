import logging
import socket

log_level: int = logging.DEBUG

if __name__ == "__main__":
    print("> Starting client")

    # Default values
    HOST = "127.0.0.1"
    PORT = 8001
    TOUT = 5

    # Setup logger
    logging.basicConfig(
            level=log_level,
            format="> %(asctime)s %(levelname)s: %(message)s"
    )

    # Attempting connection to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        client.settimeout(TOUT)

        # Data for transfer
        message = b"Ehlo Server"

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
            client.sendall(message)

    print("> Exiting")
