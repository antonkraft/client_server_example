import logging

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
    print("> Exiting")
