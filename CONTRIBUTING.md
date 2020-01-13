# Contributing to Chariot 

## Introduction

This document serves as the reference for developers who would like to get the development environment setup and understand the intended workflow required to contribute to this project. This is still a work in progress as the project evolves.

## Setting up the dev environment

These instructions are split into those for the official [front-end](#setting-up-the-front-end) and the [core](#setting-up-the-core), since the core works independent of the front-end and exposes a REST-ful API which enables any developer to write their own front-end.

### Setting up the front end

WIP

### Setting up the core

The entirety of the core is written in Python. Thus the following are required in order to have a working dev environment:

- NIX* environment (Linux, WSL, macOS terminal)
- Python (3.5 and above)
- Pip

Keep in mind that we enforce the use of python3 type hints as much as possible, to avoid obscurity.

Optionally, though strongly recommended, is to install Python's virtual environment (venv) module which will help with package management and dependency isolation. The rest of this tutorial assumes you have chosen to use a venv. 

Follow these steps to finish setting up:
1. Spin up a venv in the core folder, and activate it using any equivalent shell command to bash's `source ./bin/activate`.
2. Install all dependencies using `pip install -r requirements.txt`.
3. (WIP but intended workflow) run linters, typechecks and tests with the command `tox`. It will run using the configuration in the `tox.ini` file. If every test passes, you are ready to start contributing.

### Pushing changes

Chariot follows a Pull Request model in that all changes to the master branch must be merged from a pull request. In the future, the project will have integrated CI which must pass for changes to be accepted. In the meantime, it is paramount to ensure all `tox` checks are passing before creating a pull request.

