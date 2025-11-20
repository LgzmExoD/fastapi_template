"""
Application setup script.
Installs dependencies and configures the database.
"""

import subprocess
import sys


def run_command(cmd: str) -> None:
    """
    Execute a shell command and exit on failure.

    Args:
        cmd: Command to execute

    Raises:
        SystemExit: If command fails
    """
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"✗ Command failed: {cmd}")
        sys.exit(1)


def main() -> None:
    """Main setup workflow."""
    print("=" * 60)
    print("FastAPI Template - Setup")
    print("=" * 60)

    # Install dependencies
    print("\n[1/4] Installing dependencies...")
    run_command(f"{sys.executable} -m pip install -r requirements.txt")

    # Check database connection
    print("\n[2/4] Verifying database connection...")
    run_command(
        f'{sys.executable} -c "import asyncio; '
        f"from app.backend_pre_start import main; "
        f'asyncio.run(main())"'
    )

    # Run migrations
    print("\n[3/4] Running database migrations...")
    run_command("alembic upgrade head")

    # Create initial data
    print("\n[4/4] Creating initial data...")
    run_command(f"{sys.executable} -m app.initial_data")

    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print("\nTo start the server, run:")
    print(f"  {sys.executable} run.py")
    print("\nOr directly with uvicorn:")
    print("  uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
