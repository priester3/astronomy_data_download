from astroquery.mast import Observations
import io
import numpy as np
import pdb
import os
from tqdm import tqdm
from astropy.table import Table
from multiprocessing import Pool, cpu_count
import gzip
import shutil

need_observation_ids = np.load('mast_need_observation_ids_nomove.npy').tolist()

save_path = 'hst_data'
os.makedirs(save_path, exist_ok=True)

def gzip_fits(file_path):
    """把 FITS 压缩成 .gz，并删除原文件"""
    gz_path = file_path + ".gz"
    with open(file_path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)
    return gz_path

def download_through_id(ind):
    """单个子进程执行的任务，返回该 id 下找到的 drc 列表"""
    hst_id = need_observation_ids[ind]

    # 搜索观测数据
    obs_table = Observations.query_criteria(obs_id=hst_id)

    # 获取数据产品
    products = Observations.get_product_list(obs_table)

    # 筛选 DRC
    drc_products = Observations.filter_products(
        products,
        productSubGroupDescription="DRC",
        extension="fits"
    )
    if len(drc_products) == 0:
        return 
    
    manifest = Observations.download_products(
        drc_products,
        download_dir=save_path,
        mrp_only=False      # 设为 False 才可以下载所有产品
    )

    # 遍历并压缩所有本地 FITS 文件
    local_files = manifest['Local Path']

    for file in local_files:
        if file.endswith(".fits"):
            gz = gzip_fits(file)



if __name__ == "__main__":
    # 使用 cpu 核心数的一半，避免 MAST 过载
    num_workers = 10
    print(f"Using {num_workers} workers")

    with Pool(num_workers) as pool:
        results = list(tqdm(pool.imap(download_through_id, range(len(need_observation_ids))),
                           total=len(need_observation_ids)))
