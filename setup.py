import subprocess

from setuptools import setup

with open("README.md", "r") as fp:
    readme = fp.read()


setup(
    name="jsondataclasses",
    version=subprocess.check_output(["git", "describe", "--tags"]).decode("ascii").replace("v", "").strip(),
    url="https://github.com/issy/python-jsondataclasses",
    license="MIT",
    description="Typed JSON dataclasses",
    long_description=readme,
    long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
    readme=readme,
    packages=["jsondataclasses"],
    python_requires=">=3.9.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
