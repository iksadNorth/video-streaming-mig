#!/bin/bash


poetry add --group dev ipykernel
poetry run python -m ipykernel install --user --name=video-streaming-mig --display-name "Python (Poetry)"
poetry run jupyter notebook --no-browser --port=8888
