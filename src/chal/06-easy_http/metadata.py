import os
import subprocess

from rknazo.anura.utils import wrap_flag
from rknazo.peson.types import (
    BuildResult,
    BuildSettings,
    Context,
    LoggerConfig,
    PrerunProgram,
    ProdProperty,
)

from environ.packages.apk import ApkPackage
from environ.packages.rust import Rust

LITCRYPT_KEY = "rknazo{1t's-a-hUg3-c4@11eng3-w0rk1ng-w1th-n3tw0rk}"
KEY = "rknazo{1t's-@-GI@NT-St3p-to-f1nd-1t!}"

settings = BuildSettings(required_packages={Rust})


def build(context: Context) -> BuildResult:
    os.chdir("daemon")

    # === build ===

    flag = wrap_flag(context.flag)
    lib_rs_code = f"""
use litcrypt::{{lc, use_litcrypt}};
use once_cell::sync::Lazy;

use_litcrypt!();

pub static KEY: Lazy<String> = Lazy::new(|| lc!("{KEY}"));
pub static FLAG: Lazy<String> = Lazy::new(|| lc!("{flag}"));
"""

    with open("src/lib.rs", "w") as fp:
        fp.write(lib_rs_code)

    env = os.environ.copy()
    env["LITCRYPT_ENCRYPT_KEY"] = LITCRYPT_KEY

    subprocess.check_call(["cargo", "build", "--release"], env=env)

    # === build ===

    os.chdir("../")

    os.rename("daemon/target/release/daemon", ".daemon")

    logger = LoggerConfig(name="easy_http", stdout=True, stderr=True)
    daemon = PrerunProgram(cmd=["./.daemon"], logger=logger, daemon=True)
    prop = ProdProperty(
        required_packages={ApkPackage("tcpdump"), ApkPackage("curl")},
        prerun_programs=[daemon],
    )

    return BuildResult(artifacts=[".daemon", "tips.txt"], prop=prop)
