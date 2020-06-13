import logging
from table import get_table
import json
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()
    pl_table = get_table()
    print(pl_table)


if __name__ == "__main__":
    main()
