import os
from pathlib import Path
from tarfile import TarFile
from typing import ClassVar
from urllib.request import urlopen

from rknazo.peson.types import Package
from zstandard import ZstdDecompressor

from environ.packages.apk import ApkPackage


class _ArkariLLVM(Package):
    _build_base: ClassVar[ApkPackage] = ApkPackage("build-base")

    def __str__(self) -> str:
        return "ArkariLLVM"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _ArkariLLVM)

    def required_packages(self) -> set[Package]:
        return {self._build_base}

    def install(self) -> None:
        uname = os.uname()
        machine = uname.machine

        url = f"https://github.com/ricky8955555/Arkari/releases/download/19.1.3-obf1.6.0/arkari-llvm-19.1.3-obf1.6.0-alpine-3.21.0-{machine}-linux-musl.tar.zstd"

        with urlopen(url) as resp:
            decompressor = ZstdDecompressor()
            with decompressor.stream_reader(resp) as zstd:
                with TarFile(mode="r", fileobj=zstd) as tar:
                    tar.extractall("/")

        gcc_libs = Path(f"/usr/lib/gcc/{machine}-alpine-linux-musl/14.2.0")

        os.symlink(gcc_libs / "crtbeginS.o", "/usr/lib/crtbeginS.o")
        os.symlink(gcc_libs / "crtendS.o", "/usr/lib/crtendS.o")
        os.symlink(gcc_libs / "libgcc.a", "/usr/lib/libgcc.a")

        os.environ["PATH"] = f"/usr/local/llvm/bin:" + os.environ["PATH"]


ArkariLLVM = _ArkariLLVM()
