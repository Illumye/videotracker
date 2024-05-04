#!/bin/bash

# Check if virtual environment is activated
# If activated, install dependencies
# If not activated, create a virtual environment and install dependencies
# ">&2" is used to redirect the error message to stderr 

if [ $VIRTUAL_ENV ]; then
    echo "Virtual environment activated. Installing dependencies..."
    if [ -d "venv" ]; then
        pip install -r src/requirements.txt
        if [ $? -eq 0 ]; then
                echo "Dependencies installed."
                exit 0
        else
                >&2 echo -e "\033[31;1merror\033[0m: Failed to install dependencies."
                exit 1
        fi
    else
        >&2 echo -e "\033[31;1merror\033[0m: Failed to install dependencies."
        >&2 echo -e "\033[34;1mhint\033[0m: You may have deleted the venv folder."
        >&2 echo "      Restart your shell and re-run the script."
        exit 1
    fi

else
    echo "Non-existent virtual environment. Creating one..."
    python -m venv venv
    if [ $? -eq 0 ]; then
        echo "Created."
        echo "Please activate the virtual environment and re-run the script."
        exit 0
    else
        echo -e "\033[31;1merror\033[0m: Failed to create virtual environment."
        exit 1
    fi
fi