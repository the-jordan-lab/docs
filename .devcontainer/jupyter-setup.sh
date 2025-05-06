#!/bin/bash

echo "Setting up Jupyter environment for lab documentation..."

# Install Jupyter and required dependencies
pip install jupyter notebook jupyterlab pandas matplotlib plotly pyyaml ipywidgets

# Enable Jupyter extensions
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Set up Jupyter to auto-start in the background
mkdir -p ~/.jupyter
echo "c.NotebookApp.token = ''" > ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py

echo "Jupyter environment setup complete!"