# Missing Data Predictor
## Overview
The purpose of this project is to compare text mining and machine learning methods for populating missing data in a structured dataset, based on the information contained within a column comprising unstructured data.

## Prerequisites
- `.env` file with locations to store data (see template/env_template.txt for an example)
- Python 3.9.6

## Setup
1. Create a virtual environment with ```python3 -m venv venv```
2. Activate the venv by running ```source venv/bin/activate.csh```
3. Install dependencies via pip by running ```pip install -r requirements.txt```

Alternatively, see section below on Using the Makefile.


## Command-Line Options
`--update-config`

Use the `--update-config` flag when executing the script to force an update of the configuration file before the main application starts. This option reads the current environment variables specified in your .env file, updates the config.json file accordingly with these latest values, and then proceeds with the rest of the code. This option is particularly useful when there have been changes to the environment variables or the initial setup of the project requires generating the configuration file.

Example usage:

```bash
python main.py --update-config
```

This command should be used sparingly, only when you need to refresh the configuration file to reflect changes in the environment variables. Under normal circumstances, where the configuration remains unchanged, simply running the script without this flag is recommended to avoid unnecessary updates and to speed up the program's startup time.

## Using the Makefile

The included Makefile simplifies the process of setting up the project environment and running the application. Below are the commands you can use:

### Setting Up the Virtual Environment

- `make venv`: Creates a Python virtual environment and installs all required dependencies listed in `requirements.txt`. This command only needs to be run once at the beginning or whenever you update the dependencies in `requirements.txt`.

### Running the Application

- `make run`: Activates the virtual environment and runs the main application script (`main.py`). Ensure you've set up the virtual environment using `make venv` before running this command.

### Cleaning Up

- `make clean`: Removes Python bytecode files and the virtual environment directory. Use this command to clean up the project directory.

### Default Goal

- If you run `make` without specifying a target, it will execute the `run` target by default, thanks to the `.DEFAULT_GOAL` setting in the Makefile.

### Notes

- The Makefile uses the `.ONESHELL` special target, allowing all commands in a recipe to run in a single shell instance. This facilitates the activation of the virtual environment and the execution of subsequent commands within it, ensuring a seamless setup and run process.

- Ensure you have Python 3 and Make installed on your system to use these commands. This Makefile is designed to make it easier to manage project dependencies and streamline the execution of the code.
