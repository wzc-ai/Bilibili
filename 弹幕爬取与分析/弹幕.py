#https://www.bilibili.com/video/BV1dR4y1F7Aq/?spm_id_from=333.934.0.0&vd_source=b4c39bc93faf57124b32d95af1f46da4
import requests
from bs4 import BeautifulSoup
def get_danmu(bvid):
    api_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={get_oid(bvid)}'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')
        danmu_list = [d.text for d in soup.find_all('d')]
        return danmu_list
    return []
def get_oid(bvid):
    api_url = f'https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['data'][0]['cid']
    return None
bvid = 'BV1MN4y177PB' # 替换为实际的BV号
danmu = get_danmu(bvid)
with open(f'弹幕1.csv', 'w', encoding='utf-8') as f:
    for d in danmu:
        f.write(d + '\n')