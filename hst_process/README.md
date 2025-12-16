本项目用于从 MAST（Mikulski Archive for Space Telescopes）查询与下载 HST DRC 科学观测数据。

1. 环境配置：需要的库有 astroquery, astropy
2. 下载 [mast_need_observation_ids_nomove.npy](https://drive.google.com/file/d/1alkTCWk2wFnVfcPJcLxHo5LodVilp2yv/view?usp=drive_link)：所需下载的HST数据的观测id列表
3. 运行 mast_download_hst.py.py 进行数据下载