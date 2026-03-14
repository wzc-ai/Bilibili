import requests
import execjs

with open("up主视频爬取\w_rid.js","r",encoding="utf-8") as f:
    js_code = f.read()

ctx = execjs.compile(js_code)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}
cookies = {
}
url = "https://api.bilibili.com/x/space/wbi/arc/search"
params = {
    "pn": "1",
    "ps": "42",
    "tid": "0",
    "special_type": "",
    "order": "pubdate",
    "mid": "3493111365897099",
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
t = {
    "wbiImgKey": "c458435a75b1419ca98ab6d88b4c60d4",
    "wbiSubKey": "446140f6859f439e9dd83f7ef858d1cd"
}
params['w_rid'],params['wts']=ctx.call("XN",params,t).values()

response = requests.get(url, headers=headers, cookies=cookies, params=params)

print(response.text)
print(response)