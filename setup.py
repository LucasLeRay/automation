from setuptools import setup

with open("./README.md") as f:
    long_description = f.read()

with open("./requirements.txt") as fp:
    dependencies = [line.strip() for line in fp.readlines()]

setup(
    name="Automation tools",
    version="1.0.0",
    description="Tools to automate my processes.",
    long_description=long_description,
    author="Lucas LE RAY",
    packages=["automation"],
    install_requires=dependencies,
)
