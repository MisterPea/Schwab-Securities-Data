from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="process_brokerage_data",
    version="0.0.1",
    description="Schwab brokerage data",
    packages=['process_brokerage_data'],
    install_requires=requirements
)
