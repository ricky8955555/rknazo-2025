import subprocess

from rknazo.anura.utils import wrap_flag
from rknazo.peson.types import BuildResult, BuildSettings, Context

from environ.packages.arkari_llvm import ArkariLLVM

SEED = "rknazo{i_l0v3_sl33piN_=w=}"
KEY = [0x736C3370, 0x3E69353C, 0x67303064, 0x5C3E3C2F]


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
