from setuptools import setup, find_packages
from usb2container import (
    __AUTHOR__,
    __AUTHOR_EMAIL__,
    __URL__,
    __LICENSE__,
    __VERSION__,
    __PROJECT_NAME__,
    __DESCRIPTION__,
)

setup(
    name=__PROJECT_NAME__,
    version=__VERSION__,
    description=__DESCRIPTION__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    url=__URL__,
    packages=find_packages(),
    include_package_data=True,
    license=__LICENSE__,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "fastapi",
        "uvicorn",
        "loguru",
        "fire",
        "pydantic==0.32.2",
        "pyudevmonitor>=0.1.1",
    ],
    entry_points={"console_scripts": ["usb2container = usb2container.server:main",]},
)
