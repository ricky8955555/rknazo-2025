import os
import random
from pathlib import Path

from rknazo.anura.flag import Flag
from rknazo.anura.utils import wrap_flag
from rknazo.peson.types import BuildResult, Context

DEPTH = 30  # depth of links
COUNT = 80  # number of file at the same depth


def build(context: Context) -> BuildResult:
    def make_filename() -> str:
        flag = Flag(
            encrypted_data=bytes(random.choices(range(0xFF), k=4)),
            partial_password=bytes(random.choices(range(0xFF), k=2)),
            decrypted_data_checksum=bytes(random.choices(range(0xFF), k=2)),
            challenge_id=context.flag.challenge_id,
        )

        flag = wrap_flag(flag).encode().hex()

        if os.access(chaos / flag, 0, follow_symlinks=False):  # ensure not used.
            return make_filename()

        return flag

    root = Path()

    outdir = root / "out"
    outdir.mkdir()

    chaos = outdir / "chaos"
    chaos.mkdir()

    flag = outdir / "flag"

    # === make chain to real flag ===

    last = wrap_flag(context.flag).encode().hex()
    (chaos / last).touch()

    for _ in range(DEPTH - 1):
        filename = make_filename()
        os.symlink(last, chaos / filename)
        last = filename

    # make a relative symlink
    os.symlink(chaos.relative_to(outdir) / last, flag)

    # === make chain to real flag ===

    # === make chain to fake flags ===

    lasts: list[str] = []

    for _ in range(COUNT):
        file = make_filename()
        (chaos / file).touch()
        lasts.append(file)

    for _ in range(DEPTH - 1):
        for i in range(len(lasts)):
            last = lasts[i]
            lasts[i] = filename = make_filename()
            os.symlink(last, chaos / filename)

    # === make chain to fake flags ===

    return BuildResult(artifacts=[chaos, flag, "tips.txt"])
