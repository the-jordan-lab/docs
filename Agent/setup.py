from setuptools import setup, find_packages

setup(
    name="lab",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "chromadb",
        "biopython",
        "gitpython",
    ],
    entry_points={
        "console_scripts": [
            "lab=Agent.lab:main",
            "lab-record=Agent.lab:record_cli",
            "lab-init-extensions=Agent.init_extensions:main",
        ],
    },
    python_requires=">=3.8",
) 