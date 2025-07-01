from setuptools import setup, find_packages
import glob
import os

# Lecture de la version depuis grove/__version__.py
version = {}
with open(os.path.join("grove", "__version__.py")) as f:
    exec(f.read(), version)

setup(
    name="grove",
    version=version["__version__"],
    description="🌱 Grove : un gestionnaire de workspaces en ligne de commande.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="karamir",
    author_email="",  
    url="https://github.com/Karamir-dev/grove",
    packages=find_packages(), 
    python_requires=">=3.8",
    install_requires=[],  
    entry_points={
        "console_scripts": [
            "grove=grove.cli:main", 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    data_files=[
        ("etc/grove", glob.glob("etc/*"))
    ],
)
