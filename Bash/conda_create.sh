# From scratch
conda create -p ./env python=3.9

# From definitino file
conda env create -f env.yml -p ./env

# Install pip packages
conda env update -f pkgs.yml -p ./env