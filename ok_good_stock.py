import json
import time

import requests
import config


def good_stock(skuId, area_id):
    """
    监控库存
    :return:
    """
    url = "https://c0.3.cn/stocks"

    params = {
        "skuIds": skuId,
        "area": area_id,  # 收货地址id
        "type": "getstocks",
        "_": int(time.time() * 1000)
    }

    headers = {"Referer": f"https://item.jd.com/{skuId}.html",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/75.0.3770.142 Safari/537.36",
               }

    response = requests.get(url, params=params, headers=headers)
    # print(response.text)    # 33: 现货    34: 无货     40: 可配货
    json_dict = json.loads(response.text)
    stock_state = json_dict[skuId]['StockState']
    stock_state_name = json_dict[skuId]['StockStateName']
    return stock_state, stock_state_name


def main():
    a, b = good_stock(config.skuId, config.area_id)
    # 39 在途
    print(a, b)


if __name__ == '__main__':
    main()
