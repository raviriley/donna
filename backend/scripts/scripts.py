"""Having these commands in a Python file enables them to be run with `poetry run`."""

from __future__ import annotations

import subprocess

project_folder = "backend"

targets = f"{project_folder} scripts tests"


class TextStyle:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def lint() -> None:
    """Linting script."""

    print("🚨 Type checking with mypy...")
    subprocess.run(f"mypy {targets}", shell=True, text=True)

    print("🎨 Linting code style and formatting with ruff...")
    subprocess.run(f"ruff check {targets}", shell=True, text=True)

    # print("🔒️  Scan for security issues with bandit...")
    # subprocess.run(f"bandit -r -q {project_folder}", shell=True, text=True)


def format_code() -> None:
    """Formatting script."""

    print("🎨 Formatting code with ruff...")
    subprocess.run(f"ruff check {targets} --fix", shell=True, text=True)
    subprocess.run(f"ruff format {targets}", shell=True, text=True)

    print("✅ Formatting complete!")


def format_and_lint() -> None:
    """Runs linting and formatting in one go."""
    print(f"🎨 {TextStyle.UNDERLINE}Running formatters...{TextStyle.END}")
    format_code()
    print(f"\n🚨 {TextStyle.UNDERLINE}Running linters...{TextStyle.END}")
    lint()


def test() -> None:
    """Testing script."""
    # parser = argparse.ArgumentParser(description='Say hi.')
    # parser.add_argument('target', type=str, default="tests", help='the name of the target')
    # args = parser.parse_args()

    subprocess.run(f"pytest tests --cov={project_folder}", shell=True, text=True)


def format_lint_test() -> None:
    """Runs linting, formatting, and testing in one go."""
    print(f"🎨 {TextStyle.UNDERLINE}Running formatters...{TextStyle.END}")
    format_code()
    print(f"🚨 {TextStyle.UNDERLINE}Running linters...{TextStyle.END}")
    lint()
    print(f"🧪 {TextStyle.UNDERLINE}Running tests...{TextStyle.END}")
    test()
