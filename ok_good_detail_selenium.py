import time
from pprint import pprint

from bs4 import BeautifulSoup
from selenium import webdriver

import config
from log import logger
from ok_good_stock import good_stock
from ok_good_price import good_price


def good_detail(skuId, area_id):
    # return good detail
    good_data = {
        'id': skuId,
        'name': '',
        'cart_link': '',
        'price': '',
        'stock': '',
        'stockName': '',
    }
    # try:
    # 商品详情页
    detail_link = f"https://item.jd.com/{skuId}.html"
    logger.info(';'.join(['detail_link: ', str(detail_link)]))

    url_login = f'https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fitem.jd.com%2F{skuId}.html'

    driver = webdriver.Chrome()
    driver.get(url_login)
    time.sleep(17)

    cookies = driver.get_cookies()
    logger.info('--------'.join(['cookies: ', str(cookies)]))

    # print(type(cookies))
    # a = [{'domain': '.jd.com', 'expiry': 1924905600, 'httpOnly': False, 'name': '3AB9D23F7A4B3C9B', 'path': '/',
    #       'secure': False,
    #       'value': '3T26DYVY3ICVD33Q7NE7EUY6CB236Y4VB7SK3FHYJBSRVNV5BABPFGBNNFOZAY35Y4GWSYL4AJIY5HSQSY5Y2N62VY'},
    #      {'domain': '.jd.com', 'httpOnly': False, 'name': 'wlfstk_smdl', 'path': '/', 'secure': False,
    #       'value': '6f3x650szknfu6yw2ryagffte2wy0tt7'},
    #      {'domain': '.jd.com', 'expiry': 1608137885, 'httpOnly': False, 'name': '__jdb', 'path': '/', 'secure': False,
    #       'value': '122270672.2.16081360851671355214215|1.1608136085'},
    #      {'domain': '.jd.com', 'httpOnly': False, 'name': '__jdc', 'path': '/', 'secure': False, 'value': '122270672'},
    #      {'domain': '.jd.com', 'expiry': 1623688086, 'httpOnly': False, 'name': '__jdu', 'path': '/', 'secure': False,
    #       'value': '16081360851671355214215'},
    #      {'domain': 'passport.jd.com', 'httpOnly': False, 'name': '_t', 'path': '/', 'sameSite': 'None', 'secure': True,
    #       'value': 'VpZ9jnwoya3p8eWsSMu06yab7I7JKiCwIH9b4RZ7hBU='},
    #      {'domain': '.jd.com', 'expiry': 1623688085, 'httpOnly': False, 'name': '__jda', 'path': '/', 'secure': False,
    #       'value': '122270672.16081360851671355214215.1608136085.1608136085.1608136085.1'},
    #      {'domain': 'passport.jd.com', 'expiry': 1608136385, 'httpOnly': False,
    #       'name': 'ry0ry13r8gw3nkbrchv1608136084712cqvd', 'path': '/', 'secure': False, 'value': '147'},
    #      {'domain': 'passport.jd.com', 'httpOnly': False, 'name': '_s_id', 'path': '/', 'secure': False,
    #       'value': 'ry0ry13r8gw3nkbrchv1608136084712cqvd'},
    #      {'domain': 'passport.jd.com', 'expiry': 4761736084, 'httpOnly': False, 'name': '_c_id', 'path': '/',
    #       'secure': False, 'value': 'egviklrrj9qf62iwqfk16081360847127yqd'},
    #      {'domain': '.jd.com', 'expiry': 1609432085, 'httpOnly': False, 'name': '__jdv', 'path': '/', 'secure': False,
    #       'value': '122270672|direct|-|none|-|1608136085168'},
    #      {'domain': 'passport.jd.com', 'httpOnly': True, 'name': 'alc', 'path': '/', 'sameSite': 'None', 'secure': True,
    #       'value': '8BBFQRCdorn63prydu7w2w=='}]

    # response = requests.get(detail_link).text
    driver.get(detail_link)
    time.sleep(2)

    response = driver.page_source

    # soup = BeautifulSoup(response.text, "lxml")
    soup = BeautifulSoup(response, "html.parser")

    pretty_html = str(soup.prettify())
    # logger.info(pretty_html)
    # print(soup.prettify())

    # 产品名称
    name = soup.find('div', class_="sku-name").get_text().strip()
    good_data['name'] = name
    # 购物车链接
    # 这里没有结算，但是弄出来购物车链接之后，在浏览器访问，就会自动放进购物车
    cart_link = soup.find("a", id="InitCartUrl")['href']
    if cart_link[:2] == '//':  # '//cart.jd.com/gate.action?pid=5504364&pcount=1&ptype=1'
        cart_link = 'http:' + cart_link
    good_data['cart_link'] = cart_link

    good_data['price'] = good_price(skuId)
    good_data['stock'], good_data['stockName'] = good_stock(skuId, area_id)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f'{time.ctime()} > 商品详情')
    print(f"编号：{good_data['id']}")
    print(f"库存：{good_data['stockName']}")
    print(f"价格：{good_data['price']}")
    print(f"名称：{good_data['name']}")
    print(f"加入购物车链接：{good_data['cart_link']}")

    # {'cart_link': 'http://cart.jd.com/gate.action?pid=326467&pcount=1&ptype=1',
    #  'id': '326467',
    #  'name': '士力架 花生夹心巧克力（全家桶）礼物送女友 休闲零食员工福利 糖果460g （新旧包装随机发放）',
    #  'price': '32.89',
    #  'stock': 39,
    #  'stockName': '在途'}

    return good_data


def main():
    a = good_detail(config.skuId, config.area_id)
    pprint(a)


if __name__ == '__main__':
    main()
