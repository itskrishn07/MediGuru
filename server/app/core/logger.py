import logging
import sys

def setup_logging():
    # Setup global logging to print to stdout with structured format
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

# Run logger configuration on import
setup_logging()
