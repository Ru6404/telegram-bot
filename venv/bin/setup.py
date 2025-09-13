from setuptools import setup
import subprocess
import sys

def run_setup_env():
    try:
        subprocess.run([sys.executable, "setup_env.py"], check=True)
    except Exception as e:
        print("⚠️ Ошибка при запуске setup_env.py:", e)

run_setup_env()

setup(
    name="my_project",
    version="0.1",
    install_requires=[],
)
