from brew.packages import install_formulae, install_casks


class TestPackages:
    def test_install_formulae_dry_run(self):
        install_formulae(["git", "curl"], dry_run=True)

    def test_install_casks_dry_run(self):
        install_casks(["temurin"], dry_run=True)

    def test_install_empty_list(self):
        install_formulae([], dry_run=True)
        install_casks([], dry_run=True)
