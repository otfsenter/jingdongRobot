import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import config
from log import logger


def get_jxj(soup):
    # //惊喜金 我也不知道是个啥玩意
    return '1'


def get_btSupport(soup):
    if len(soup.find_all(class_='payment-item', attrs={'onlinepaytype': '1'})) == 0:
        if "payment-item-disabled" in str(soup.find_all(class_='payment-item', attrs={'onlinepaytype': '1'})):
            return '0'
    else:
        return '1'


def order_info(skuId, submit=False):
    """
    下单
    :param submit: 是否提交订单
    :return: 是否下单成功
    """
    # get order info detail, and submit order
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(f'{time.ctime()} > 订单详情')

    order_url = 'http://trade.jd.com/shopping/order/getOrderInfo.action'
    payload = {
        'rid': str(int(time.time() * 1000)),
    }

    url_login = f'https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fitem.jd.com%2F{skuId}.html'

    driver = webdriver.Chrome()
    driver.get(url_login)
    time.sleep(17)

    cookies_list = driver.get_cookies()

    cookies_dict = {}
    for i in cookies_list:
        name = i.get('name', '')
        value = i.get('value', '')
        cookies_dict.setdefault(name, value)

    # 获取预下单页面
    # rs = requests.get(order_url, params=payload, cookies=cookies_dict).text
    driver.get(order_url)
    time.sleep(3)

    rs = driver.page_source


    # soup = BeautifulSoup(rs.text, "lxml")
    soup = BeautifulSoup(rs, "html.parser")
    # logger.info(str(soup.prettify()))

    # order summary
    payment = soup.find(id='sumPayPriceId').text  # TODO
    detail = soup.find(class_='fc-consignee-info')

    if detail:
        snd_usr = detail.find(id='sendMobile').text  # 收货人
        snd_add = detail.find(id='sendAddr').text  # 收货地址

        print('应付款：{0}'.format(payment))
        print(snd_usr)
        print(snd_add)

    # just test, not real order
    if not submit:
        return False

    # order info
    sopNotPutInvoice = soup.find(id='sopNotPutInvoice')['value']

    btSupport = get_btSupport(soup)
    ignorePriceChange = soup.find(id='ignorePriceChange')['value']
    riskControl = soup.find(id='riskControl')['value']
    jxj = get_jxj(soup)

    data = {
        'overseaPurchaseCookies': '',
        'vendorRemarks': [],  # 貌似是订单备注    [{"venderId":"632952","remark":""}]
        'submitOrderParam.sopNotPutInvoice': sopNotPutInvoice,  # 货票分离开关值  false or true
        'submitOrderParam.trackID': 'TestTrackId',  # 写死
        'submitOrderParam.get_ignorePriceChange': ignorePriceChange,
        'submitOrderParam.btSupport': btSupport,  # 是否支持白条
        'submitOrderParam.eid': config.eid,  # 设备id
        'submitOrderParam.fp': config.fp,  # ?
        'riskControl': riskControl,
        'submitOrderParam.jxj': jxj,
        'submitOrderParam.trackId': 'cc46bf84f6274988c7cde62fce0cc11a',
    }
    # print(data)
    order_url = 'http://trade.jd.com/shopping/order/submitOrder.action'
    rp = requests.post(order_url, data=data, cookies=cookies_dict, headers={
        'Referer': 'https://trade.jd.com/shopping/order/getOrderInfo.action?rid=' + payload['rid'],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    })
    print(rp.text)

    if rp.status_code == 200:
        js = json.loads(rp.text)
        if js['success']:
            print('下单成功！订单号：{0}'.format(js['orderId']))
            print('请前往京东官方商城付款')
            # send_email('下单成功', f'应付款：{payment}, 请前往京东官方商城付款')
            return True
        else:
            print('下单失败！<{0}: {1}>'.format(js['resultCode'], js['message']))
            if js['resultCode'] == '60017':
                # 60017: 您多次提交过快，请稍后再试
                time.sleep(1)
    else:
        print('请求失败. StatusCode:', rp.status_code)

    return False


def main():
    order_info(config.skuId)


if __name__ == '__main__':
    main()
