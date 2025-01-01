import os
import subprocess
from urllib.request import urlopen

from rknazo.peson.types import Package


class _Rust(Package):
    def __str__(self) -> str:
        return f"Rust"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Rust)

    def install(self) -> None:
        with urlopen("https://sh.rustup.rs") as resp:
            sh = resp.read()

        cmd = ["sh", "-s", "--", "-y"]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE)

        assert process.stdin

        process.stdin.write(sh)
        process.stdin.close()

        ret = process.wait()

        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)

        home = os.environ["HOME"]
        os.environ["PATH"] = f"{home}/.cargo/bin:" + os.environ["PATH"]

    def required_packages(self) -> set[Package]:
        return set()


Rust = _Rust()
