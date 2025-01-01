import os

from rknazo.anura.utils import generate_flags
from rknazo.peson.builder import Builder

FLAGS = [b"mU", b"7u", b"Mi", b"51", b"N3n", b"Om3", b"d3t0"]

CHALDIR = "chal"
CHALLENGES = [
    "00-my_users",
    "01-dont_get_lost",
    "02-pipe_worker",
    "03-say_millions_of_yes_to_me!",
    "04-sleep_lover",
    "05-patch_your_neko",
    "06-easy_http",
]

OUTDIR = "out/chal"

PASSWORD = ">w<{h@v3_fUn_@_pl@y1n_rkN@z0-2o2S}=w="


def main() -> None:
    builder = Builder()
    flags = generate_flags(FLAGS, PASSWORD)
    dirs = [os.path.join(CHALDIR, challenge) for challenge in CHALLENGES]
    builder.build_all(dirs, flags, OUTDIR)


if __name__ == "__main__":
    main()
