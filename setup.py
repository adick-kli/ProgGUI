# setup.py
"""
Setup-Script für ProgGUI
Macht das Projekt als Python-Package installierbar
"""

from setuptools import setup, find_packages
from pathlib import Path

# Readme laden
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="ProgGUI",
    version="1.0.0",
    description="Professional AT32UC3A1512 Programmer GUI for Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="adick-kli",
    author_email="adick60@gmail.com",
    url="https://github.com/adick-kli/ProgGUI",
    license="MIT",
    
    packages=find_packages(),
    python_requires=">=3.9",
    
    install_requires=[
        # tkinter ist bereits in Python enthalten
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "build": [
            "pyinstaller>=6.0.0",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "proggui=src.app.gui:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)