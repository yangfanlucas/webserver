import requests, random, json
from hashlib import md5

def trans(query, to_lang):
    appid = ''
    appkey = ''
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    s = appid + query + str(salt) + appkey
    sign = md5(s.encode('utf-8')).hexdigest()
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': 'auto', 'to': to_lang, 'salt': salt, 'sign': sign}
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    trans_result = result["trans_result"]
    dst_list = []
    for x in trans_result:
        dst = "" + x["dst"]
        dst_list.append(dst)
    dst = "\n".join(str(s) for s in dst_list)
    return dst
