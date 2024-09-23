#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
利用requests+bs4爬取Boss直聘数据
author: gxcuizy
date: 2020-06-18
"""
import configparser
import logging
import pathlib
import requests
from bs4 import BeautifulSoup
from common.SslConfig import _addSsl,_ssl_session

# SSL 配置
current_dir = pathlib.Path(__file__).parent
cert = current_dir / 'ssl' / 'psbc_crt.pem'
key = current_dir / 'ssl' / 'psbc_key.pem'
bundle = current_dir / 'ssl' / 'psbc_full.pem'
session = _ssl_session(cert, key, bundle)


"""
深圳 5-10年
https://www.zhipin.com/c101280600/?query=java&experience=106&page=1&ka=page-1
北京 5-10年
https://www.zhipin.com/c101010100/?query=java&experience=106&page=1&ka=page-1
重庆 5-10年
https://www.zhipin.com/c101040100/?query=java&experience=106&page=1&ka=page-1
沈阳 5-10年
https://www.zhipin.com/c101070100/?query=java&experience=106&page=1&ka=page-1
成都 5-10年
https://www.zhipin.com/c101270100/?query=java&experience=106&page=1&ka=page-1

郑州 5-10年
https://www.zhipin.com/c101180100/?query=java&experience=106&page=1&ka=page-1

长沙 5-10年
https://www.zhipin.com/c101250100/?query=java&experience=106&page=1&ka=page-1

西安 5-10年
https://www.zhipin.com/c101110100/?query=java&experience=106&page=1&ka=page-1


"""
class GetBossData(object):
    """爬取10页的Boss直聘职位数据"""
    domain = 'https://www.zhipin.com'
    base_url = 'https://www.zhipin.com/c101110100/?experience=106&query='
    position = ''
    # 代理IP地址
    proxies_ip = '58.220.95.30'
    proxies_port = '10174'

    def __init__(self, position):
        self.position = position

    def get_url_html(self, url, cookie):
        """请求页面html"""
        ip_url = self.proxies_ip + ':' + str(self.proxies_port)
        proxies = {'http': 'http://' + ip_url, 'https': 'https://' + ip_url}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'cookie': cookie
        }
        # request = requests.get(url=url, headers=header, proxies=proxies, timeout=3)
        request = requests.get(url=url, headers=header, timeout=3)

        html = False
        if request.status_code == 200:
            html = request.content
        return html

    def run(self):
        """执行入口"""
        page_list = range(1, 15)
        # 打开文件，准备写入
        dict_file = open('job.md', 'a', encoding='UTF-8')
        # 清空文件内容
        dict_file.seek(0)
        dict_file.truncate()
        dict_file.write('| 岗位 | 区域 | 薪资 | 年限信息 | 公司名称 | 公司信息 | 链接 |')
        dict_file.write('\n| --- | --- | --- | --- | --- | --- | --- |')
        # 分页爬取数据
        msg = 'wt2=DwKd0swLlNWIszpUm56EcuXBjOuoEUkZrFCZ2IRv_LRJPucq8Ko8DuhGijKqUsth22tQyB4k14s9eqAnEp9Fu2Q~~; wbg=0; zp_at=UdVC9kKiwUJIBCLxlxckkfN4TaIlA0vBprVWyXySm5o~; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1726797652,1726812446,1726820219; HMACCOUNT=62A8AF414BB7B780; __g=-; lastCity=100010000; __l=l=%2Fwww.zhipin.com%2Fc101250100%2F%3Fexperience%3D106%26query%3Djava%26page%3D10%26ka%3Dpage-10&s=3&friend_source=0&s=3&friend_source=0; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1726825041; __c=1726820220; __a=46972178.1646708282.1726812442.1726820220.122.7.41.108; bst=V2QtsuEuz13FdgXdJryBgdKSuw7D3fzQ~~|QtsuEuz13FdgXdJryBgdKSuw7D3VxQ~~; __zp_stoken__=1c48fw4oaDFpHF1oVEmVsWcKFfMOIwrxswrtrUWtywrnCqsOHw4DCvFXDhU3CtVJiw4HCtMK5ZsKrZ8Khwq5OwpvCnmTCrcKkw7nCscKzWsO1w4PCtcODw6vDhsOdwprEg8Kkw7fDgcO1wp%2FDtcK4w6PDhsO6wrvDkcKqw7TCisOTwpLDs8K9w5nClcWBw73FgsKPw6zDvMO4xIXEt8OxxKPDhcOowq%2FEu8Kuw5TFsMSnxbHFh8SWxIjDg8KbRjYLFhUWDhcKCQoSEg8PEBgMFRYVDQoXGBcPOS%2FEhMSGIDtFOUMpVUxLEVVmXlReSRBoU1I7OmUYDGA6KURDOz7CuUTDiAvDiEPDhxPDgT7DiGRDQz5Dw4Z%2BMDDDhsK4MRkKw4PCkRfCu8OXaMOEw6IPw45Zw5HChcO1wrnCrDBFPcK%2BxYQ5RhlIRkU8Pjs7RUYpOz%2FDlFnDinzDrcOHwp4uPiY9Rj5ESEVGPkJGOzI%2BQ3czRjsuOhYWEwsMNjnCv8K7w4PDmkY%2B@@@@@@wt2=DwKd0swLlNWIszpUm56EcuXBjOuoEUkZrFCZ2IRv_LRJPucq8Ko8DuhGijKqUsth22tQyB4k14s9eqAnEp9Fu2Q~~; wbg=0; zp_at=UdVC9kKiwUJIBCLxlxckkfN4TaIlA0vBprVWyXySm5o~; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1726797652,1726812446,1726820219; HMACCOUNT=62A8AF414BB7B780; __g=-; lastCity=100010000; __c=1726820220; __l=l=%2Fwww.zhipin.com%2Fc101110100%2F%3Fexperience%3D106%26query%3Djava%26page%3D1%26ka%3Dpage-1&s=3&friend_source=0&s=3&friend_source=0; __a=46972178.1646708282.1726812442.1726820220.123.7.42.109; bst=V2QtsuEuz13FdgXdJryBgdKSuw7D3VxQ~~|QtsuEuz13FdgXdJryBgdKSuw7DzTzA~~; __zp_stoken__=1c48fw4nDo8KzWzsYaA4TWWtnfnnCvMK7dsOEak1scMOCwqvCu8K%2Fw4ZOw4hRwrZQWcOEwrDCulzCtGbCncKtVMKkwp9gwq7CnsSCwrTCr1nDq8K8w7xVwrbCnsOzZcO3wpXClsK7w6bCpcKQw4LClMKRw5vCp8OpwpbDjsOCw5jCncOkwqnFgMKqxYHCl8S8wrLDrMKfxK%2FCocS1wpPErcO1w5HCn8SiwrTDi8WtxJvFssWIw4fDssK%2Fwpk8LQoKFgwVFhYKGAkTExASDwkJFQsWCwsXCRg8M8SDw7wnOjk6PTJYWEwPTmdiU2RSDVxUUEQ7WRcWZzs1Qz1EP8OFQ8K6FMOFP8OIDcK6P8K8Yz08Pz%2FDhcKENy3CusK3LyILwr%2FCkgnDhMOWXMODw6AYw49lw5J6HMK8w6YwO0bCv8WAOjwiRTpGRkU6R0Y8Mjopw5Nnw5F8IjIsRBpCRjw%2BPDpGPEA6SDI8PDIwRj00RgkWFRUYKTnCucOFwr%2FDpUY8; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1726825257@@@@@@wt2=DwKd0swLlNWIszpUm56EcuXBjOuoEUkZrFCZ2IRv_LRJPucq8Ko8DuhGijKqUsth22tQyB4k14s9eqAnEp9Fu2Q~~; wbg=0; zp_at=UdVC9kKiwUJIBCLxlxckkfN4TaIlA0vBprVWyXySm5o~; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1726797652,1726812446,1726820219; HMACCOUNT=62A8AF414BB7B780; __g=-; lastCity=100010000; __c=1726820220; __l=l=%2Fwww.zhipin.com%2Fc101110100%2F%3Fexperience%3D106%26query%3Djava%26page%3D4%26ka%3Dpage-4&s=3&friend_source=0&s=3&friend_source=0; __a=46972178.1646708282.1726812442.1726820220.124.7.43.110; bst=V2QtsuEuz13FdgXdJryBgdKSuw7DzTzA~~|QtsuEuz13FdgXdJryBgdKSuw7DvUwQ~~; __zp_stoken__=1c48fw4pawqBoOgtjFxBceGTCh8KGwrnDiHHCuXVQd2vCu8K4wrrDhMOBV8K7VMKpS2TCv8Ktw4VfwqlZwqDCslfCmcKkXcKxwpnDu8Kvwq5mw7DDgcSHWMKpwpnDqlrDtsKKwpHDgsOZwqjCk8OFwonCjsOawpzDrsKPw5HDvsO8w7vFh07FiMKTw5bDg8SqwrnErMKaw7fCpMSaw4fEn8OqxJ3CrcOXwrfDksWyxJrFrcWDwrTDrsK%2Bwqc%2FOBULCQ8QCRcVExQQEhMVFhYMChAPGAoMDg1HMsSAw78eRTxFOitLVVcMV1xjUGdLEllPSzlIXAwRXkg4QDo5RMOIQMK9CcK6PsK7CsODRMK5YDpBRD7CusKHLjLCu8KsLBsYwr7CjQ7CucOJWcOAw5sNw5Row419GMOHVDRAP8OExL1FPxs6OzlBQEVGOT8rRSrDkGTDjMKHE8K7w4UwRBtBP0A%2BOTk%2FQEA7RytAPBsvPzk0RwoPERUVKkTCvcOFwr7Dpj9A; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1726825274@@@@@@wt2=DwKd0swLlNWIszpUm56EcuXBjOuoEUkZrFCZ2IRv_LRJPucq8Ko8DuhGijKqUsth22tQyB4k14s9eqAnEp9Fu2Q~~; wbg=0; zp_at=UdVC9kKiwUJIBCLxlxckkfN4TaIlA0vBprVWyXySm5o~; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1726797652,1726812446,1726820219; HMACCOUNT=62A8AF414BB7B780; __g=-; lastCity=100010000; __c=1726820220; __l=l=%2Fwww.zhipin.com%2Fc101110100%2F%3Fexperience%3D106%26query%3Djava%26page%3D7%26ka%3Dpage-7&s=3&friend_source=0&s=3&friend_source=0; __a=46972178.1646708282.1726812442.1726820220.125.7.44.111; bst=V2QtsuEuz13FdgXdJryBgdKSuw7DvUwQ~~|QtsuEuz13FdgXdJryBgdKSuw7DvSwQ~~; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1726825295; __zp_stoken__=1c48fw4lbOV4%2FD2UWFl10ZsKGwoDDgMOEd8K8b0lzbcK6wq7Cv8OIw4dWw4FVwq1NYcOFwqzDgVnCrGPCmcK2UcKcwppcwrXCn8O6wrXCq2LDqsOEw71Rwq3Cn8OrZMOzwo7Cl8ODw6PCocKXw4PCjMKYw5%2FCoMOswo7Di8Ksw6vCqsOSwrHDosO7w6LCksORwo7DjcKsxJvCi8Oow4LDscO5xK7EgsWDwrHDk8WsxJ%2FFqcWFwqjDtsK7wqM5NQ8ODQkNExIRFREWFxcTFxANDgoODg8QDBA9N8O8w7kfPz1BQCpRVFMOVmJmTGFKDGBLTTw%2BXRAXXz4xPEA8OsOBPMK7DMOEO8K%2FEMOCOsOAXEBEOjvCvsKBLyzCvsKwLhoOwrvCiQzCvMOTYMK8w50Qw4phw4l7a8K%2Fw484Oj7CusS8QTkaRD49Rz0%2FQz05Kj8sw4xmw4l9bMK%2BPC06HkU5PUhAPTk9Rj5DLT1CHis5PCpCDgkUDxQuRsOAwr%2FCu8OiOT0%3D'
        cookie_data = msg.split('@@@@@@')
        for page in page_list:
            print('开始爬取第' + str(page) + '页数据')
            boss_url = self.base_url + str(self.position) + '&page=' + str(page) + '&ka=page-' + str(page)
            # F12打开调试模式，手动刷新网页获取cookie，然后替换
            if page < 4:
                cookie_val = cookie_data[0]
            elif page < 7:
                cookie_val = cookie_data[1]
            elif page < 10:
                cookie_val = cookie_data[2]
            else:
                cookie_val = cookie_data[3]
            try:
                html = self.get_url_html(boss_url, cookie_val)
                print(f'调用{boss_url}')
            except Exception as e:
                print(f'调用{boss_url}报错:')
                print(e)
            soup = BeautifulSoup(html, 'html.parser')
            print("标题:", soup.title.string)
            # 招聘职位列表
            job_list = soup.select('.job-list ul li')
            for job_li in job_list:
                # 单条职位信息
                url = self.domain + job_li.select('.job-title a')[0].attrs['href']
                title = job_li.select('.job-title a')[0].get_text()
                area = job_li.select('.job-title .job-area')[0].get_text()
                salary = job_li.select('.job-limit .red')[0].get_text()
                year = job_li.select('.job-limit p')[0].get_text()
                company = job_li.select('.info-company h3')[0].get_text()
                industry = job_li.select('.info-company p')[0].get_text()
                info = {
                    'title': title,
                    'area': area,
                    'salary': salary,
                    'year': year,
                    'company': company,
                    'industry': industry,
                    'url': url
                }
                print(info)
                # 写入职位信息
                info_demo = '\n| %s | %s | %s | %s | %s | %s | %s |'
                dict_file.write(info_demo % (title, area, salary, year, company, industry, url))
        dict_file.close()


# 程序主入口
if __name__ == '__main__':
    # 实例化
    job_name = input('请输入职位关键字：').strip()
    if job_name == '':
        print('关键字为空，请重新尝试')
        exit(0)
    gl = GetBossData(job_name)
    # 执行脚本
    gl.run()
