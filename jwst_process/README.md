本项目用于从 MAST（Mikulski Archive for Space Telescopes）查询与下载 JWST 科学观测数据，并生成对应的观测目录（catalog）。

1. 环境配置：需要的库有 astroquery, astropy
2. 设置 config: 配置 workspace_dir，项目的主工作目录
3. 运行 1_catalog.py 生成需要下载的观测目录（catalog）
4. 运行 2_download.py 进行数据下载