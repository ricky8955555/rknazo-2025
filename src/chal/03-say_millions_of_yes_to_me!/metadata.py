import subprocess

from rknazo.anura.utils import wrap_flag
from rknazo.peson.types import BuildResult, BuildSettings, Context

from environ.packages.arkari_llvm import ArkariLLVM

SEED = "rknazo{s@Y_Mi11i0n5_0f_Ye5_tO_m3!}"
KEY = [0x72726B6B, 0x6E617A6F, 0x69733E3E, 0x66756E69]


settings = BuildSettings(required_packages={ArkariLLVM})


def build(context: Context) -> BuildResult:
    # generate data.h
    flag = wrap_flag(context.flag)

    subprocess.check_call(
        [
            # fmt: off
            "python3", "scripts/data_h_gen.py",
            "--flag", flag,
            "--key", *map(str, KEY),
            "--seed", SEED,
            "-o", "src/data.h",
            # fmt: on
        ]
    )

    # build challenge binary
    subprocess.check_call(
        [
            # fmt: off
            "clang",
            "-mllvm", "-irobf-indbr", "-mllvm", "-level-indbr=3",
            "-mllvm", "-irobf-icall", "-mllvm", "-level-icall=3",
            "-mllvm", "-irobf-indgv", "-mllvm", "-level-indgv=3",
            "-mllvm", "-irobf-cse",
            "-mllvm", "-irobf-cff",
            "-mllvm", "-irobf-cie", "-mllvm", "-level-cie=3",
            "-mllvm", "-irobf-cfe", "-mllvm", "-level-cfe=3",
            "-o", "challenge",
            "-O3",
            "-s",
            "src/challenge.c",
            # fmt: on
        ]
    )

    return BuildResult(artifacts=["challenge"])
