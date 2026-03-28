
import subprocess

def init_migration():
    subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", "init"],
        check=True
    )

def upgrade_head():
    subprocess.run(
        ["alembic", "upgrade", "head"],
        check=True
    )