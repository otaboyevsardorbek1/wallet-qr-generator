from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="wallet-qr-generator",
    version="1.0.0",
    author="CryptoQR Team",
    author_email="support@cryptoqr.dev",
    description="Professional CLI tool for generating beautiful crypto wallet QR codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otaboyevsardorbek1/wallet-qr-generator/",
    project_urls={
        "Bug Tracker": "https://github.com/otaboyevsardorbek1/wallet-qr-generator/issues",
        "Documentation": "https://github.com/otaboyevsardorbek1/wallet-qr-generator/wiki",
        "Source Code": "https://github.com/otaboyevsardorbek1/wallet-qr-generator/",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "walletqr=wallet_qr.cli:main",
            "crypto-qr=wallet_qr.cli:main",
            "wallet-qr-generator=wallet_qr.cli:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "qr-code",
        "crypto",
        "wallet",
        "cryptocurrency",
        "bitcoin",
        "ethereum",
        "cli",
        "generator",
        "crypto-wallet",
        "qr-generator",
    ],
    license="MIT",
    platforms=["any"],
)