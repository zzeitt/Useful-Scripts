# Full export
conda env export > env.yml

# Neatly export (but lose 'pip')
conda env export --from-history > env.yml