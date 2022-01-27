"""
Export a Conda environment with --from-history, but also append
Pip-installed dependencies

Exports only manually-installed dependencies, excluding build versions, but
including Pip-installed dependencies.

Lots of issues requesting this functionality in the Conda issue tracker, no
sign of progress (as of March 2020).

TODO (?): support command-line flags -n and -p
"""
import re
import subprocess
import sys
import yaml
import fire


def export_env(s_conda, history_only=False):
    cmd = [s_conda, 'env', 'export']
    if history_only:
        cmd.append('--from-history')

    cp = subprocess.run(cmd, stdout=subprocess.PIPE)
    try:
        cp.check_returncode()
    except:
        raise
    else:
        return yaml.safe_load(cp.stdout)


def _is_history_dep(d, history_deps):
    if not isinstance(d, str):
        return False
    d_prefix = re.sub(r'=.*', '', d)
    return d_prefix in history_deps


def _get_pip_deps(full_deps):
    for dep in full_deps:
        if isinstance(dep, dict) and 'pip' in dep:
            return dep


def _combine_env_data(env_data_full, env_data_hist):
    deps_full = env_data_full['dependencies']
    deps_hist = env_data_hist['dependencies']
    deps = [dep for dep in deps_full if _is_history_dep(dep, deps_hist)]

    pip_deps = _get_pip_deps(deps_full)

    env_data = {}
    env_data['channels'] = env_data_full['channels']
    env_data['dependencies'] = deps
    env_data['dependencies'].append(pip_deps)

    return env_data


def main(
    s_conda='/home/zeit/miniconda3/condabin/conda',
    s_save=None):
    '''
    Run `whereis conda` to find the location of the conda executable.
    Give `s_conda` the path to the conda executable.
    '''
    env_data_full = export_env(s_conda)
    env_data_hist = export_env(s_conda, True)
    env_data = _combine_env_data(env_data_full, env_data_hist)
    if s_save:
        with open(s_save, 'w') as y:
            yaml.dump(env_data, y)
    else:
        yaml.dump(env_data, sys.stdout)


if __name__ == '__main__':
    fire.Fire(main)
