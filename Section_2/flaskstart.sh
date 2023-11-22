#!/bin/bash
# This script activates the virtual environment and starts the Flask app

source flask/bin/activate

export FLASK_APP=run.py
export FLASK_DEBUG=1
flask run --port=1024
