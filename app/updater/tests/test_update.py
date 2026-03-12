from updater.update import run_update


class TestRunUpdate:
    def test_dry_run_completes(self):
        run_update(dry_run=True)
