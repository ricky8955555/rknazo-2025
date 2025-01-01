import subprocess

from rknazo.peson.types import Package


class ApkPackage(Package):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"Apk<{self.name}>"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ApkPackage) and self.name == other.name

    def install(self) -> None:
        subprocess.check_call(["apk", "add", "--no-cache", "--update", self.name])

    def required_packages(self) -> set[Package]:
        return set()
