import os
import shutil

from rknazo.peson.conf import Configurator

CHALDIR = "chal"
BINDIR = "bin"
INSTDIR = "/usr/local/bin"


def main() -> None:
    conf = Configurator()
    challenges = os.scandir(CHALDIR)
    conf.configure_all(challenges)

    for bin in os.scandir(BINDIR):
        dest = os.path.join(INSTDIR, bin.name)
        shutil.move(bin, dest)
        os.chmod(dest, 0o700)

    shutil.rmtree(BINDIR)


if __name__ == "__main__":
    main()
