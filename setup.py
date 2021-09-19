import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="porth",
    version="0.1.0",
    description="It's like Forth but in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tsoding/porth",
    author="Alexey Kutepov",
    author_email="reximkut@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["."],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "porth=porth:main",
        ]
    },
)
