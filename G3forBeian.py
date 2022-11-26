import time
import datetime
import argparse
from colorama import Fore
import requests
from lxml import etree
import csv

Yellow = Fore.YELLOW
Reset = Fore.RESET

base_url = "https://beian.tianyancha.com/search/"
# 全局计数器
num = 1


def search(body, csvwriter):
    global num
    for tr in body:
        print(f'{num}, {"".join(tr.xpath("./td[4]//text()"))}, {"".join(tr.xpath("./td[5]/span/text()"))}')
        csvwriter.writerow([num, "".join(tr.xpath("./td[2]/a/text()")), "".join(tr.xpath("./td[3]//text()")),
                            "".join(tr.xpath("./td[4]//text()")), "".join(tr.xpath("./td[5]/span/text()"))])
        num = num + 1


# 判断搜索的公司，是否存在备案信息，存在的备案信息是否为多页
def page_search(company_name, csvwriter, sleeptime, headers):
    Complete_search_url = base_url + company_name
    Search_resp = requests.get(Complete_search_url, headers=headers)
    Search_resp_tree = etree.HTML(Search_resp.text)
    Search_resp_tree_tbody = Search_resp_tree.xpath("//*[@id=\"search\"]/div[2]/table/tbody/tr")
    # 判断是否存在备案信息
    if len(Search_resp_tree_tbody) == 0:
        return False
    else:

        Multi_page_judgment = Search_resp_tree.xpath("//*[@id=\"search\"]/div[3]/ul")
        # 判断是否为多页内容
        if len(Multi_page_judgment) == 0:
            search(Search_resp_tree_tbody, csvwriter)
            time.sleep(sleeptime)
        else:
            search(Search_resp_tree_tbody, csvwriter)
            time.sleep(sleeptime)
            for Multi_page_url in Search_resp_tree.xpath("//*[@id=\"search\"]/div[3]/ul/li/a/@href")[1:-1]:
                Multi_page_resp = requests.get(Multi_page_url, headers=headers)
                Multi_page_resp_tree = etree.HTML(Multi_page_resp.text)
                Multi_page_tree_tbody = Multi_page_resp_tree.xpath("//*[@id=\"search\"]/div[2]/table/tbody/tr")
                search(Multi_page_tree_tbody, csvwriter)
                time.sleep(sleeptime)
        return True


def company_name_search(company_name, sleeptime, headers):
    f = open(f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_result.csv', mode="a+")
    csvwriter = csv.writer(f)
    csvwriter.writerow(["序号", "网站备案/许可证号", "主办单位名称", "网站名称", "网站域名"])
    page_search(company_name, csvwriter, sleeptime, headers)
    f.close()


def file_readline(file_path, sleeptime, header):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            line = f.readlines()
            print("共获取了%d个目标" % (len(line)), '\n')
            rf = open(f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_result.csv', mode="a+")
            csvwriter = csv.writer(rf)
            csvwriter.writerow(["序号", "网站备案/许可证号", "主办单位名称", "网站名称", "网站域名"])
        for company_name in line:
            company_name = company_name.strip()
            if page_search(company_name, csvwriter, sleeptime, header):
                print(f"{company_name}执行结束")
            else:
                print("不存在备案内容")
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    finally:
        try:
            if f:
                f.close()
        except:
            pass


def display_banner():
    banne_text = rbanne_text = r"""
  ▄████  ██▀███   ███▄ ▄███▓
 ██▒ ▀█▒▓██ ▒ ██▒▓██▒▀█▀ ██▒    备案查询工具
▒██░▄▄▄░▓██ ░▄█ ▒▓██    ▓██░    
░▓█  ██▓▒██▀▀█▄  ▒██    ▒██     Coded By G3RM4
░▒▓███▀▒░██▓ ▒██▒▒██▒   ░██▒    
 ░▒   ▒ ░ ▒▓ ░▒▓░░ ▒░   ░  ░    Ice technology
  ░   ░   ░▒ ░ ▒░░  ░      ░
░ ░   ░   ░░   ░ ░      ░       https[:]//github.com/mengmeng9921/
      ░    ░            ░                                       
"""
    print(f"{Yellow}{banne_text}{Reset}")


def cmdline(known=False):
    parser = argparse.ArgumentParser(description=display_banner())
    parser.add_argument(
        '-n',
        '--companyname',
        help='-n companyname',
        type=str
    )
    parser.add_argument(
        '-nf',
        '--companynamefile',
        help='-nf 1.txt',
        type=str
    )
    parser.add_argument(
        '-s',
        '--sleeptime',
        help='-s 1',
        type=int,
        default=0
    )
    parser.add_argument(
        '-c',
        '--cookie',
        help='-c cookie',
        type=str,
        default=""
    )
    opt = parser.parse_args()
    return opt


def main():
    headers = {
        'Connection': 'close',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    f = None
    opt = cmdline()
    try:
        if opt.cookie:
            print(opt.cookie)
            headers.update({'cookie': opt.cookie})
        if opt.companynamefile:
            file_readline(opt.companynamefile, opt.sleeptime, headers)
            print("所有任务全部结束～")
        elif opt.companyname:
            company_name_search(opt.companyname, opt.sleeptime, headers)
            print("所有任务全部结束～")
        else:
            print("参数输入错误，使用-h获取详细参数～")
    except:
        print("未知异常，请联系作者～")


if __name__ == '__main__':
    main()
