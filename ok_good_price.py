import json

import requests
import config


def good_price(skuId):
    # get good price
    url = 'http://p.3.cn/prices/mgets'
    payload = {
        'type': 1,
        'skuIds': 'J_' + skuId,
    }
    price = '?'

    response = requests.get(url, params=payload)
    resp_txt = response.text.strip()
    json_dict = json.loads(resp_txt[1:-1])  # 去掉首尾的[]
    price = json_dict['p']

    return price


def main():
    price = good_price(config.skuId)
    # 32.89
    print(price)


if __name__ == '__main__':
    main()
