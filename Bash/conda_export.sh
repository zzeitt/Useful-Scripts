# Full export
conda env export > env.yml

# Neatly export (but lose 'pip')
conda env export --from-history > env.yml

# Minimal export (include 'pip')
pip install pyyaml
pip install fire
python Python/conda_export_minimal.py --s_save=env.yaml