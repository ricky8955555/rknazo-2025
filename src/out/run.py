import os

from rknazo.peson.logger import file_logger
from rknazo.peson.runner import Runner

LOGDIR = "/var/log/rknazo"
CHALDIR = "chal"


def main() -> None:
    os.mkdir(LOGDIR)
    logger = file_logger(LOGDIR)

    challenges = os.scandir(CHALDIR)

    runner = Runner(challenges, logger)
    runner.run(["sh"])


if __name__ == "__main__":
    main()
