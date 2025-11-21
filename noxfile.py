import nox
import os

# PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.12"]
PYTHON_VERSIONS = ["3.12"]

TEST_DEPENDENCIES = [
    "pytest",
    "pytest-cov",
    "black",
    "flake8",
    "mypy",
]

ML_DEPENDENCIES = [
    "numpy",
    "pandas",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "tensorflow",
]

@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.install("poetry")
    session.run("poetry", "install", "--no-interaction", "--no-root")
    session.run("pytest")

@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    session.install("flake8")
    session.run("flake8", "src", "tests")

@nox.session(python=PYTHON_VERSIONS)
def black(session):
    session.install("black")
    session.run("black", "src", "tests")

# Nox session for type checking with mypy
@nox.session(python=PYTHON_VERSIONS)
def mypy(session):
    session.install("mypy")
    session.run("mypy", "src")

