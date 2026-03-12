import platform
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Platform(Enum):
    MACOS_ARM = "darwin_arm64"
    MACOS_INTEL = "darwin_x86_64"
    LINUX = "linux"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class BrewPaths:
    prefix: Path
    bin: Path
    cellar: Path
    opt: Path

    @property
    def brew_executable(self) -> Path:
        return self.bin / "brew"


def get_platform() -> Platform:
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system != "darwin":
        if system == "linux":
            return Platform.LINUX
        return Platform.UNSUPPORTED

    if machine in ("arm64", "aarch64"):
        return Platform.MACOS_ARM
    return Platform.MACOS_INTEL


def get_brew_paths(plat: Platform | None = None) -> BrewPaths:
    if plat is None:
        plat = get_platform()

    if plat == Platform.MACOS_ARM:
        prefix = Path("/opt/homebrew")
    else:
        prefix = Path("/usr/local")

    return BrewPaths(
        prefix=prefix,
        bin=prefix / "bin",
        cellar=prefix / "Cellar",
        opt=prefix / "opt",
    )


@dataclass
class PackageLists:
    formulae: list[str] = field(default_factory=list)
    casks: list[str] = field(default_factory=list)


FORMULAE: list[str] = [
    "git",
    "curl",
    "docker",
    "ruby",
    "perl",
    "python",
    "sbt",
    "apache-spark",
]

CASKS: list[str] = [
    "temurin",
]
