from astroquery.mast import Observations
from astropy.table import Table
import pdb

import yaml
import os

# 加载配置文件
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 获取配置参数
base_dir = config['all']['workspace_dir']
catalog_cfg = config['jwst']['catalog_cfg']
output_file = config['jwst']['catalog_cfg']['output_file']

# 查询数据
obs_table = Observations.query_criteria(
        calib_level=catalog_cfg['calib_level'],
        dataproduct_type=catalog_cfg['dataproduct_type'],
        intentType=catalog_cfg['intentType'],
        obs_collection=catalog_cfg['obs_collection']
    )

Table(obs_table).write(os.path.join(base_dir, output_file), format='votable')







