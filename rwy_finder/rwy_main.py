import logging
import os
from datetime import datetime

from dotenv import load_dotenv

from rwy_finder.rwy_pipeline import run_rwy_pipeline


def main() -> None:
    """Entry point for the RWY Finder application."""
    load_dotenv()
    configure_logging()
    data_path = os.getenv('DATA_PATH', 'data')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_dir = os.path.join(data_path, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f'Output directory: {output_dir}')
    run_rwy_pipeline(data_path, output_dir)


def configure_logging() -> None:
    """Configure logging for console and file output."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    # Console handler (INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # File handler (DEBUG)
    fh = logging.FileHandler('rwy_finder_debug.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
