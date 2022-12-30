#encoding: utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mikatools",
    version="1.0.1",
    author="Mika Hämäläinen",
    author_email="mika.hamalainen@helsinki.fi",
    description="Quick methods for everyday Python programming",
    long_description=long_description,
    install_requires=['requests', "tqdm", "cryptography"],
    long_description_content_type="text/markdown",
    url="https://github.com/mikahama/mikatools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
    "mikatools": ["countries.json"]
    },
)