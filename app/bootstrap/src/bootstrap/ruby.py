from logger import get_logger
from settings import get_brew_paths, get_platform
from shell import ZshrcEditor

log = get_logger("bootstrap.ruby")

SECTION_HEADER = "Ruby Path variables"


def configure_ruby(editor: ZshrcEditor) -> None:
    paths = get_brew_paths(get_platform())
    ruby_bin = paths.opt / "ruby" / "bin"
    ruby_lib = paths.opt / "ruby" / "lib"
    ruby_include = paths.opt / "ruby" / "include"

    log.info("Configuring Ruby environment")
    editor.remove_section(f"# {SECTION_HEADER}")
    editor.add_section(SECTION_HEADER, [
        f'export PATH="{ruby_bin}:$PATH"',
        f'export LDFLAGS="-L{ruby_lib}"',
        f'export CPPFLAGS="-I{ruby_include}"',
    ])
