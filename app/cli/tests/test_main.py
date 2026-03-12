from click.testing import CliRunner

from cli.main import cli


class TestCli:
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "bootstrap" in result.output.lower()

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_check_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["check", "--help"])
        assert result.exit_code == 0
        assert "dry-run" in result.output.lower()

    def test_run_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0


class TestUpdateCli:
    def test_update_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["update", "--help"])
        assert result.exit_code == 0
        assert "--dry-run" in result.output

    def test_update_dry_run(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["update", "--dry-run"])
        assert result.exit_code == 0


class TestScheduleCli:
    def test_schedule_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["schedule", "--help"])
        assert result.exit_code == 0
        assert "hourly" in result.output
        assert "daily" in result.output
        assert "weekly" in result.output

    def test_unschedule_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["unschedule", "--help"])
        assert result.exit_code == 0

    def test_status_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["status", "--help"])
        assert result.exit_code == 0

    def test_status_shows_not_scheduled(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "NOT scheduled" in result.output or "ACTIVE" in result.output
