import click

from logger import get_logger
from bootstrap.runner import run_bootstrap, check_bootstrap
from updater.update import run_update
from updater.scheduler import schedule_updates, unschedule_updates, get_schedule_status

log = get_logger("cli")


@click.group()
@click.version_option(version="0.1.0", prog_name="dev-bootstrap")
def cli():
    """macOS development environment bootstrap toolkit."""


@cli.command()
def run():
    """Run the full bootstrap process."""
    log.info("Starting bootstrap...")
    try:
        run_bootstrap()
    except Exception as exc:
        log.error("Bootstrap failed: %s", exc)
        raise SystemExit(1) from exc


@cli.command()
def check():
    """Dry-run: preview what the bootstrap would do without making changes."""
    log.info("Running bootstrap check (dry-run)...")
    check_bootstrap()


@cli.command()
@click.option("--dry-run", is_flag=True, help="Preview updates without applying them.")
def update(dry_run):
    """Update Homebrew and upgrade all managed packages."""
    log.info("Starting package update...")
    try:
        run_update(dry_run=dry_run)
    except Exception as exc:
        log.error("Update failed: %s", exc)
        raise SystemExit(1) from exc


@cli.command()
@click.option(
    "--interval",
    type=click.Choice(["hourly", "daily", "weekly"]),
    default="weekly",
    show_default=True,
    help="How often to run auto-updates.",
)
@click.option("--dry-run", is_flag=True, help="Preview schedule setup without installing it.")
def schedule(interval, dry_run):
    """Set up automatic updates via macOS LaunchAgent.

    Installs a LaunchAgent plist in ~/Library/LaunchAgents/ that periodically
    runs `dev-bootstrap update` in the background. Logs are written to
    ~/Library/Logs/dev-bootstrap/.
    """
    log.info("Setting up auto-update schedule (%s)...", interval)
    try:
        info = schedule_updates(interval, dry_run=dry_run)
        if info.installed:
            click.echo(f"Auto-update scheduled: every {info.interval_seconds}s")
            click.echo(f"  Plist:      {info.plist_path}")
            click.echo(f"  Executable: {info.dev_bootstrap_path}")
            click.echo("  Logs:       ~/Library/Logs/dev-bootstrap/")
        else:
            click.echo("Dry-run complete. No changes made.")
    except Exception as exc:
        log.error("Schedule setup failed: %s", exc)
        raise SystemExit(1) from exc


@cli.command()
@click.option("--dry-run", is_flag=True, help="Preview removal without actually removing.")
def unschedule(dry_run):
    """Remove the auto-update LaunchAgent."""
    removed = unschedule_updates(dry_run=dry_run)
    if removed:
        click.echo("Auto-update schedule removed.")
    else:
        click.echo("No auto-update schedule was installed.")


@cli.command()
def status():
    """Show current auto-update schedule status."""
    info = get_schedule_status()
    if info.installed:
        hours = info.interval_seconds / 3600 if info.interval_seconds else 0
        click.echo("Auto-update is ACTIVE")
        click.echo(f"  Interval: every {info.interval_seconds}s ({hours:.0f}h)")
        click.echo(f"  Plist:    {info.plist_path}")
        click.echo(f"  Command:  {info.dev_bootstrap_path}")
    else:
        click.echo("Auto-update is NOT scheduled.")
        click.echo("  Run 'dev-bootstrap schedule' to enable.")


if __name__ == "__main__":
    cli()
