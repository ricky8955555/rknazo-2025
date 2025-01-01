from rknazo.anura.utils import wrap_flag
from rknazo.peson.types import BuildResult, Context, ProdProperty


def build(context: Context) -> BuildResult:
    flag = wrap_flag(context.flag).encode().hex()
    script_file = "configure.sh"

    script = f"adduser -D -H -h /dev/null -s /sbin/nologin -g {flag} flag".strip()

    with open(script_file, "w") as fp:
        fp.write(script)

    prop = ProdProperty(
        configurations=[
            ["sh", script_file],
            ["rm", "-f", script_file],
        ]
    )

    return BuildResult(artifacts=[script_file, "tips.txt"], prop=prop)
