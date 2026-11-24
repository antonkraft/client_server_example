import logging
import socket

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

                # Print message from client, if available
                data = connection.recv(1024)
                if data:
                    print(data.decode(UTF8))

    print("> Shutting down")
