set dotenv-load

default:
    @just --list

# Install all workspace packages
sync:
    uv sync

# Run all tests across all packages (or a single package)
test pkg="*":
    uv run pytest app/{{pkg}}/tests/ -v --tb=short

# Run all tests with coverage report
test-cov:
    uv run pytest app/*/tests/ --cov=app --cov-report=term-missing --tb=short

# Run pylint across all packages
lint:
    uv run pylint -rn -sn --rcfile development/.pylintrc app/*/src/

# Run all pre-commit checks manually
pre-commit:
    uv run pre-commit run --all-files --config development/.pre-commit-config.yaml

# Set up git hooks
setup-hooks:
    git config core.hooksPath .hooks

# Run the bootstrap (connects to macOS, installs tools)
run:
    uv run dev-bootstrap run

# Dry-run: preview what the bootstrap would do
check:
    uv run dev-bootstrap check

# Update all managed Homebrew packages
update:
    uv run dev-bootstrap update

# Set up automatic updates (hourly | daily | weekly)
schedule interval="weekly":
    uv run dev-bootstrap schedule --interval {{interval}}

# Remove the auto-update schedule
unschedule:
    uv run dev-bootstrap unschedule

# Show auto-update schedule status
status:
    uv run dev-bootstrap status
