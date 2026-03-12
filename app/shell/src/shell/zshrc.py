import re
import shutil
from pathlib import Path

from logger import get_logger

log = get_logger("shell.zshrc")

ZSHRC_PATH = Path.home() / ".zshrc"


class ZshrcEditor:
    """Safe editor for ~/.zshrc with backup support and section-based management."""

    def __init__(self, path: Path | None = None, *, dry_run: bool = False):
        self.path = path or ZSHRC_PATH
        self.dry_run = dry_run
        self._lines: list[str] = []
        self._loaded = False

    def load(self) -> "ZshrcEditor":
        if self.path.exists():
            self._lines = self.path.read_text().splitlines()
            log.info("Loaded %d lines from %s", len(self._lines), self.path)
        else:
            self._lines = []
            log.info("No existing %s found, starting fresh", self.path)
        self._loaded = True
        return self

    def backup(self) -> Path | None:
        if not self.path.exists():
            return None
        backup_path = self.path.with_suffix(".zshrc.bak")
        if self.dry_run:
            log.info("[DRY RUN] Would back up %s -> %s", self.path, backup_path)
            return backup_path
        shutil.copy2(self.path, backup_path)
        log.info("Backed up %s -> %s", self.path, backup_path)
        return backup_path

    def remove_section(self, header_comment: str) -> "ZshrcEditor":
        """Remove a block that starts with a comment header and its associated export/alias lines."""
        if not self._loaded:
            self.load()

        pattern = re.compile(re.escape(header_comment))
        new_lines: list[str] = []
        skipping = False

        for line in self._lines:
            if pattern.search(line):
                skipping = True
                continue
            if skipping and (line.startswith("export ") or line.startswith("alias ") or line.strip() == ""):
                continue
            skipping = False
            new_lines.append(line)

        removed = len(self._lines) - len(new_lines)
        if removed:
            log.info("Removed %d lines for section '%s'", removed, header_comment)
        self._lines = new_lines
        return self

    def add_section(self, header_comment: str, lines: list[str]) -> "ZshrcEditor":
        """Append a commented section with the given lines."""
        if not self._loaded:
            self.load()

        self._lines.append("")
        self._lines.append(f"# {header_comment}")
        self._lines.extend(lines)
        log.info("Added section '%s' with %d lines", header_comment, len(lines))
        return self

    def remove_blank_lines(self) -> "ZshrcEditor":
        if not self._loaded:
            self.load()
        self._lines = [line for line in self._lines if line.strip()]
        return self

    def save(self) -> None:
        if self.dry_run:
            log.info("[DRY RUN] Would write %d lines to %s", len(self._lines), self.path)
            for line in self._lines:
                log.info("  %s", line)
            return

        self.path.write_text("\n".join(self._lines) + "\n")
        log.info("Wrote %d lines to %s", len(self._lines), self.path)

    def reload_shell_hint(self) -> None:
        log.info("Run 'source %s' to apply changes", self.path)
