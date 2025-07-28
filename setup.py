from setuptools import setup, find_packages

setup(
    name="stellar-stmt",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",
        "python-dotenv",
        "sqlalchemy>=2.0.0",
        "pytest",
        "pytest-cov",
        "coverage"
    ],
)