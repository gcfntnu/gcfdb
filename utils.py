
from os.path import join, abspath, dirname
from os import makedirs, environ
import sys
import collections
import yaml
from datetime import datetime


from snakemake.logging import logger
from snakemake.workflow import srcdir
from snakemake.utils import update_config, min_version

min_version("5.1.2")

if 'EXT_DIR' not in locals():
    EXT_DIR = environ.get('GCF-EXT') or config.get('ext_dir', 'ext')
TMPDIR = environ.get('TMPDIR') or config.get('tmpdir')

def update_config2(config, extra_config):
    """Recursively update dictionary config with overwrite_config.

    From Snakemake codebase (update_config), this does not overwrite if key exist

    See
    http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    for details.

    Args:
      config (dict): dictionary to update
      overwrite_config (dict): dictionary whose items will overwrite those in config

    """
    
    def _update(d, u):
        for (key, value) in u.items():
            if (isinstance(value, collections.Mapping)):
                d[key] = _update(d.get(key, {}), value)
            else:
                if not key in d:
                    d[key] = value
        return d
    return _update(config, extra_config)
