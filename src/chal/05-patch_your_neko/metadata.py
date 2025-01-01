import subprocess

from rknazo.anura.utils import wrap_flag
from rknazo.peson.types import BuildResult, BuildSettings, Context

from environ.packages.arkari_llvm import ArkariLLVM

SEED = "rknazo{P@tcH_y0u3_k@T}"
KEY = [0x7472692D, 0x74743030, 0x64796E61, 0x70406368]


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

    # build shared lib
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
            "-o", "lib.so",
            "-O3",
            "-fPIC",
            "-shared",
            "src/lib.c",
            # fmt: on
        ]
    )

    return BuildResult(artifacts=["lib.so", "tips.txt"])
