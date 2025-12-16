import pdb
from tqdm import tqdm
import requests
import yaml
import os
from astropy.io.votable import parse_single_table
# 加载配置文件

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 获取配置参数
base_dir = config['all']['workspace_dir']
download_cfg = config['jwst']['download_cfg']
catalog_cfg = config['jwst']['catalog_cfg']
download_tag = os.path.join(base_dir, download_cfg['download_tag'])
os.makedirs(download_tag, exist_ok=True)
jwst_data_dir = os.path.join(base_dir, config['jwst']['catalog_cfg']['output_file'])

votable = parse_single_table(jwst_data_dir).to_table()

dataurl_index = votable.colnames.index('dataURL')
observation_id_index = votable.colnames.index('obs_id')

zipped_tuples = list(zip(votable.columns[observation_id_index], votable.columns[dataurl_index]))

# 下载文件函数
def download_and_upload_to_ceph(ind):
    observation_id, data_url = zipped_tuples[ind]
    seg_url = data_url[:-8] + 'segm.fits'

    urls = [f"https://mast.stsci.edu/api/v0.1/Download/file?uri={seg_url}",
            f"https://mast.stsci.edu/api/v0.1/Download/file?uri={data_url}"]

    download_directory = os.path.join(download_tag, observation_id)

    for url in urls:
        pdb.set_trace()
        try:
            filename = url.split('/')[-1]
            filepath = os.path.join(download_directory, filename)
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                os.makedirs(download_directory, exist_ok=True)
                total_size = int(response.headers.get('content-length', 0))
                with open(filepath, 'wb') as f, tqdm(
                    total=total_size, unit='B', unit_scale=True, desc=filename
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))
                print(f"Download complete: {filename}")
            else:
                print(f"Download failed: {filename}, status code: {response.status_code}")

        except Exception as e:
            print(f"Error downloading {filename}: {e}")

for i in range(len(zipped_tuples)):
    download_and_upload_to_ceph(i)

print("All downloads complete!")





