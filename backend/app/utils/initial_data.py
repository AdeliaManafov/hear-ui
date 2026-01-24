import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initial user creation removed as user/auth model was removed.
def init() -> None:
    logger.info("Initial data creation for users has been removed.")


def main() -> None:
    logger.info("Initial data setup skipped (auth removed).")


if __name__ == "__main__":
    main()
