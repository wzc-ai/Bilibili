"""
B站数据工具箱 — 整合抓取与分析平台
Flask Web Application
"""

from flask import Flask, render_template, jsonify, request, Response
import requests as http_requests
import re
import hashlib
import time
import os
import json
import urllib.parse
from collections import Counter
import execjs

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open("up主视频爬取\w_rid.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

# ─── Common Headers ──────────────────────────────────────────
cookies = {
    "buvid3": "DB41F544-FA24-EBEF-028C-F1778920FA4917154infoc",
    "b_nut": "1753171117",
    "_uuid": "C6FE553E-4DF3-1C72-1F10F-5F856D1F7106134575infoc",
    "buvid_fp": "f43a5dda453873fe2eb30a82ec0e95af",
    "enable_web_push": "DISABLE",
    "DedeUserID": "1338119500",
    "DedeUserID__ckMd5": "920c2bfd51a1a6cb",
    "theme-tip-show": "SHOWED",
    "rpdid": "0zbfVFLfJ4|17CNFQsGh|J6|3w1UE7Uq",
    "theme-avatar-tip-show": "SHOWED",
    "LIVE_BUVID": "AUTO3717534353952047",
    "theme-switch-show": "SHOWED",
    "hit-dyn-v2": "1",
    "buvid4": "844F741D-2482-3AF1-7786-B45F39670BE418045-025072215-HfgoDIUW78O8mrOHyVbQbSp9CXCjxU4FLkal1JsnFcIEn/S6YqRir+IBqxecIacx",
    "CURRENT_BLACKGAP": "0",
    "theme_style": "dark",
    "ogv_device_support_hdr": "0",
    "home_feed_column": "5",
    "SESSDATA": "22a86e47%2C1788358530%2C6124e%2A31CjB_QKrMU2zpV3KbUCl6PeMJmkS2d3Mf92mqRxUJkfoOZCF8ButP90Fr1jtZiTLtUPcSVjdyTzA1VTZCZ0F0Y1VxWDlydDdvNUpyZXhGbktzREJfZzdta2ZSVGY2RllaakNnNVk2ZFoxY0JDakVGdGpLcURFeXp5c3h0OFh2V2NrLVU3d0huMnpBIIEC",
    "bili_jct": "f298622e50d679d3b81bbe7ad751d4d2",
    "PVID": "2",
    "browser_resolution": "1707-791",
    "ogv_device_support_dolby": "0",
    "CURRENT_QUALITY": "112",
    "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzMyMzU4NTAsImlhdCI6MTc3Mjk3NjU5MCwicGx0IjotMX0.wqjptAZ1VD31hVAuebp9CayeaBCcOqG1BVVMxRQgejU",
    "bili_ticket_expires": "1773235790",
    "sid": "8e4xx320",
    "CURRENT_FNVAL": "4048",
    "bp_t_offset_1338119500": "1177432741231198208",
    "b_lsid": "CEACE69D_19CCDE53D89"
}
BILIBILI_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com',
}

# ─── WBI Signature (Pure Python) ────────────────────────────

# MIXIN_KEY_ENC_TAB = [
#     46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
#     27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
#     37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
#     22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
# ]


# def get_mixin_key(orig: str) -> str:
#     return ''.join(orig[i] for i in MIXIN_KEY_ENC_TAB)[:32]


# def wbi_sign(params: dict, img_key: str, sub_key: str) -> dict:
#     mixin_key = get_mixin_key(img_key + sub_key)
#     wts = str(int(time.time()))
#     params['wts'] = wts
#     params = dict(sorted(params.items()))
#     # Strip special chars per Bilibili spec
#     filtered = {}
#     for k, v in params.items():
#         v_str = str(v)
#         v_str = re.sub(r"[!'()*]", '', v_str)
#         filtered[k] = v_str
#     query = '&'.join(f'{k}={v}' for k, v in filtered.items())
#     w_rid = hashlib.md5((query + mixin_key).encode()).hexdigest()
#     params['w_rid'] = w_rid
#     return params


# ─── Pages ───────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ─── UP主视频 API ────────────────────────────────────────────

@app.route('/api/up/videos')
def get_up_videos():
    mid = request.args.get('mid', '').strip()
    page = request.args.get('page', '1')
    page_size = request.args.get('page_size', '30')
    order = request.args.get('order', 'pubdate')

    if not mid:
        return jsonify({'code': -1, 'message': '请输入UP主ID'})

    t = {
        "wbiImgKey": "c458435a75b1419ca98ab6d88b4c60d4",
        "wbiSubKey": "446140f6859f439e9dd83f7ef858d1cd"
    }

    params = {
        "pn": page,
        "ps": page_size,
        "tid": "0",
        "special_type": "",
        "order": order,
        "mid": str(mid),
        "index": "0",
        "keyword": "",
        "order_avoided": "true",
        "platform": "web",
        #"web_location": "333.1387",
        # "dm_img_list": "\\[{\"x\":1571,\"y\":316,\"z\":0,\"timestamp\":3674,\"k\":66,\"type\":0},{\"x\":1584,\"y\":329,\"z\":13,\"timestamp\":3881,\"k\":91,\"type\":1},{\"x\":1730,\"y\":476,\"z\":156,\"timestamp\":4210,\"k\":107,\"type\":0},{\"x\":2623,\"y\":1171,\"z\":125,\"timestamp\":4310,\"k\":92,\"type\":0},{\"x\":3063,\"y\":1701,\"z\":157,\"timestamp\":4410,\"k\":106,\"type\":0},{\"x\":3387,\"y\":2154,\"z\":347,\"timestamp\":4511,\"k\":72,\"type\":0},{\"x\":4816,\"y\":613,\"z\":612,\"timestamp\":5701,\"k\":64,\"type\":0},{\"x\":4691,\"y\":719,\"z\":507,\"timestamp\":5802,\"k\":106,\"type\":0},{\"x\":4020,\"y\":751,\"z\":96,\"timestamp\":5904,\"k\":101,\"type\":0},{\"x\":3690,\"y\":1554,\"z\":208,\"timestamp\":6071,\"k\":78,\"type\":0},{\"x\":4238,\"y\":2169,\"z\":762,\"timestamp\":6193,\"k\":93,\"type\":0},{\"x\":3582,\"y\":1496,\"z\":88,\"timestamp\":6294,\"k\":60,\"type\":0},{\"x\":4437,\"y\":2308,\"z\":888,\"timestamp\":6396,\"k\":113,\"type\":0},{\"x\":3244,\"y\":539,\"z\":940,\"timestamp\":7891,\"k\":94,\"type\":0},{\"x\":3773,\"y\":1762,\"z\":1089,\"timestamp\":7992,\"k\":89,\"type\":0},{\"x\":3151,\"y\":1618,\"z\":160,\"timestamp\":8092,\"k\":116,\"type\":0},{\"x\":4490,\"y\":2976,\"z\":1488,\"timestamp\":8194,\"k\":102,\"type\":0},{\"x\":3665,\"y\":2142,\"z\":667,\"timestamp\":8818,\"k\":122,\"type\":0},{\"x\":4390,\"y\":1856,\"z\":1987,\"timestamp\":8919,\"k\":89,\"type\":0},{\"x\":2760,\"y\":74,\"z\":399,\"timestamp\":9022,\"k\":100,\"type\":0},{\"x\":5107,\"y\":2679,\"z\":1972,\"timestamp\":10298,\"k\":69,\"type\":0},{\"x\":3562,\"y\":2251,\"z\":480,\"timestamp\":10399,\"k\":69,\"type\":0},{\"x\":4086,\"y\":2937,\"z\":955,\"timestamp\":10500,\"k\":107,\"type\":0},{\"x\":4676,\"y\":3525,\"z\":1551,\"timestamp\":10850,\"k\":79,\"type\":0},{\"x\":3609,\"y\":2241,\"z\":698,\"timestamp\":10951,\"k\":82,\"type\":0},{\"x\":2846,\"y\":1230,\"z\":426,\"timestamp\":11052,\"k\":72,\"type\":0},{\"x\":2334,\"y\":581,\"z\":26,\"timestamp\":11159,\"k\":94,\"type\":0},{\"x\":3219,\"y\":2001,\"z\":571,\"timestamp\":11260,\"k\":62,\"type\":0},{\"x\":4768,\"y\":3891,\"z\":1948,\"timestamp\":11360,\"k\":96,\"type\":0},{\"x\":4697,\"y\":3848,\"z\":1839,\"timestamp\":11461,\"k\":120,\"type\":0},{\"x\":4471,\"y\":3643,\"z\":1596,\"timestamp\":11561,\"k\":121,\"type\":0},{\"x\":3335,\"y\":2517,\"z\":453,\"timestamp\":11663,\"k\":75,\"type\":0},{\"x\":5064,\"y\":4255,\"z\":2178,\"timestamp\":13034,\"k\":94,\"type\":0},{\"x\":4796,\"y\":4094,\"z\":1842,\"timestamp\":13135,\"k\":117,\"type\":0},{\"x\":7144,\"y\":6869,\"z\":3875,\"timestamp\":13235,\"k\":109,\"type\":0},{\"x\":6788,\"y\":7139,\"z\":3734,\"timestamp\":13336,\"k\":95,\"type\":0},{\"x\":5944,\"y\":6796,\"z\":3319,\"timestamp\":13436,\"k\":81,\"type\":0},{\"x\":6570,\"y\":7531,\"z\":3526,\"timestamp\":14673,\"k\":79,\"type\":0},{\"x\":5421,\"y\":5287,\"z\":2258,\"timestamp\":14774,\"k\":64,\"type\":0},{\"x\":7412,\"y\":7209,\"z\":4272,\"timestamp\":14876,\"k\":79,\"type\":0},{\"x\":5692,\"y\":5432,\"z\":2539,\"timestamp\":14976,\"k\":123,\"type\":0},{\"x\":5658,\"y\":5285,\"z\":2453,\"timestamp\":15077,\"k\":68,\"type\":0},{\"x\":7284,\"y\":6897,\"z\":4075,\"timestamp\":15481,\"k\":123,\"type\":0},{\"x\":4242,\"y\":3085,\"z\":1342,\"timestamp\":15582,\"k\":98,\"type\":0},{\"x\":3688,\"y\":2106,\"z\":844,\"timestamp\":15682,\"k\":94,\"type\":0},{\"x\":3012,\"y\":1253,\"z\":170,\"timestamp\":15783,\"k\":124,\"type\":0},{\"x\":7054,\"y\":5239,\"z\":4196,\"timestamp\":15884,\"k\":121,\"type\":0},{\"x\":7264,\"y\":5426,\"z\":4360,\"timestamp\":15984,\"k\":97,\"type\":0},{\"x\":7638,\"y\":5741,\"z\":4681,\"timestamp\":16085,\"k\":88,\"type\":0},{\"x\":4007,\"y\":2110,\"z\":1050,\"timestamp\":16186,\"k\":121,\"type\":0}\\]",
        # "dm_img_str": "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
        # "dm_cover_img_str": "QU5HTEUgKE1pY3Jvc29mdCwgTWljcm9zb2Z0IEJhc2ljIFJlbmRlciBEcml2ZXIgKDB4MDAwMDAwOEMpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpR29vZ2xlIEluYy4gKE1pY3Jvc29mdC",
        # "dm_img_inter": "{\"ds\":\\[{\"t\":7,\"c\":\"dnVpX2J1dHRvbiB2dWlfYnV0dG9uLS1hY3RpdmUgdnVpX2J1dHRvbi0tYWN0aXZlLWJsdWUgdnVpX2J1dHRvbi0tbm8tdHJhbnNpdGlvbiB2dWlfcGFnZW5hdGlvbi0tYnRuIHZ1aV9wYWdlbmF0aW9uLS1idG4tbn\",\"p\":\\[5208,8,6561\\],\"s\":\\[9,179,18\\]}\\],\"wh\":\\[4429,6408,35\\],\"of\":\\[4867,6798,463\\]}",
    }
    params['w_rid'],params['wts']=ctx.call("XN",params,t).values()

    try:
        resp = http_requests.get(
            'https://api.bilibili.com/x/space/wbi/arc/search',
            params=params,
            headers=BILIBILI_HEADERS,
            timeout=10,
            cookies=cookies
        )
        print(resp.text)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})


@app.route('/api/up/info')
def get_up_info():
    mid = request.args.get('mid', '').strip()
    if not mid:
        return jsonify({'code': -1, 'message': '请输入UP主ID'})
    try:
        resp = http_requests.get(
            f'https://api.bilibili.com/x/web-interface/card?mid={mid}',
            headers=BILIBILI_HEADERS,
            timeout=10,
            cookies=cookies
        )
        print(resp.text)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})


# ─── 弹幕 API ───────────────────────────────────────────────

@app.route('/api/danmaku/fetch')
def fetch_danmaku():
    bvid = request.args.get('bvid', '').strip()
    if not bvid:
        return jsonify({'code': -1, 'message': '请输入BV号'})

    try:
        # Step 1 — BV号 → cid
        pagelist_url = f'https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp'
        resp = http_requests.get(pagelist_url, headers=BILIBILI_HEADERS, timeout=10)
        data = resp.json()
        if data.get('code') != 0:
            return jsonify({'code': -1, 'message': f"视频信息获取失败: {data.get('message', '')}"})

        cid = data['data'][0]['cid']
        title = data['data'][0].get('part', '')

        # Step 2 — cid → danmaku XML
        dm_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
        dm_resp = http_requests.get(dm_url, headers=BILIBILI_HEADERS, timeout=10)
        dm_resp.encoding = 'utf-8'

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(dm_resp.text, 'xml')
        danmaku_list = [d.text for d in soup.find_all('d')]

        return jsonify({
            'code': 0,
            'data': {
                'bvid': bvid,
                'cid': cid,
                'title': title,
                'count': len(danmaku_list),
                'danmaku': danmaku_list,
            },
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})


@app.route('/api/danmaku/analyze', methods=['POST'])
def analyze_danmaku():
    body = request.get_json(silent=True) or {}
    danmaku_list = body.get('danmaku', [])
    top_n = body.get('top_n', 80)

    if not danmaku_list:
        return jsonify({'code': -1, 'message': '没有弹幕数据'})

    try:
        import jieba
        all_words = []
        for dm in danmaku_list:
            words = jieba.lcut(str(dm))
            all_words.extend(w for w in words if len(w) > 1)

        counter = Counter(all_words)
        top_words = counter.most_common(top_n)

        return jsonify({
            'code': 0,
            'data': {
                'total_words': len(all_words),
                'unique_words': len(counter),
                'top_words': [{'word': w, 'count': c} for w, c in top_words],
            },
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})


@app.route('/api/danmaku/export', methods=['POST'])
def export_danmaku():
    body = request.get_json(silent=True) or {}
    danmaku_list = body.get('danmaku', [])
    filename = body.get('filename', '弹幕导出.csv')

    if not danmaku_list:
        return jsonify({'code': -1, 'message': '没有弹幕数据'})

    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for dm in danmaku_list:
            f.write(str(dm) + '\n')

    return jsonify({'code': 0, 'message': f'已导出 {len(danmaku_list)} 条弹幕到 {filename}'})


# ─── CSV / 数据 ─────────────────────────────────────────────

@app.route('/api/csv/list')
def list_csv_files():
    csv_files = []
    for root, _, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith('.csv'):
                path = os.path.join(root, f)
                rel = os.path.relpath(path, BASE_DIR)
                csv_files.append({
                    'name': f,
                    'path': rel.replace('\\', '/'),
                    'size': os.path.getsize(path),
                })
    return jsonify({'code': 0, 'data': csv_files})


@app.route('/api/csv/read')
def read_csv():
    filename = request.args.get('file', '')
    if not filename:
        return jsonify({'code': -1, 'message': '请指定文件'})

    filepath = os.path.join(BASE_DIR, filename.replace('/', os.sep))
    if not os.path.exists(filepath):
        return jsonify({'code': -1, 'message': '文件不存在'})

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return jsonify({'code': 0, 'data': lines, 'count': len(lines)})
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)})


# ─── Main ────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
