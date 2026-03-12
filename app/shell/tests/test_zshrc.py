from shell.zshrc import ZshrcEditor


class TestZshrcEditor:
    def test_load_nonexistent(self, tmp_path):
        zshrc = tmp_path / ".zshrc"
        editor = ZshrcEditor(zshrc)
        editor.load()
        assert editor._lines == []

    def test_load_existing(self, tmp_path):
        zshrc = tmp_path / ".zshrc"
        zshrc.write_text("export FOO=bar\n")
        editor = ZshrcEditor(zshrc)
        editor.load()
        assert editor._lines == ["export FOO=bar"]

    def test_backup(self, tmp_path):
        zshrc = tmp_path / ".zshrc"
        zshrc.write_text("original content\n")
        editor = ZshrcEditor(zshrc)
        backup = editor.backup()
        assert backup is not None
        assert backup.exists()

    def test_backup_dry_run(self, tmp_path):
        zshrc = tmp_path / ".zshrc"
        zshrc.write_text("original content\n")
        editor = ZshrcEditor(zshrc, dry_run=True)
        backup = editor.backup()
        assert backup is not None
        assert not backup.exists()

    def test_add_section(self, tmp_path):
        zshrc = tmp_path / ".zshrc"
        editor = ZshrcEditor(zshrc)
        editor.load()
        editor.add_section("Ruby Path variables", [
            'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"',
        ])
        editor.save()
        content = zshrc.read_text()
        assert "# Ruby Path variables" in content
        assert 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' in content

    def test_remove_section(self, tmp_path):
        zshrc = tmp_path / ".zshrc"
        zshrc.write_text(
            "# keep this\n"
            "# Ruby Path variables\n"
            'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"\n'
            "# also keep\n"
        )
        editor = ZshrcEditor(zshrc)
        editor.load()
        editor.remove_section("# Ruby Path variables")
        editor.save()
        content = zshrc.read_text()
        assert "Ruby Path" not in content
        assert "keep this" in content
        assert "also keep" in content

    def test_dry_run_does_not_write(self, tmp_path):
        zshrc = tmp_path / ".zshrc"
        editor = ZshrcEditor(zshrc, dry_run=True)
        editor.load()
        editor.add_section("Test", ["export X=1"])
        editor.save()
        assert not zshrc.exists()
