# -*- coding: utf-8 -*-
import requests


def get_headers():
    headers = {'host': "bbs.nga.cn",
               'connection': "keep-alive",
               'cache-control': "no-cache",
               'upgrade-insecure-requests': "1",
               'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
               'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               'referer': "http://bbs.ngacn.cc/misc/adpage_insert_2.html?http://bbs.ngacn.cc/read.php?tid=13427591&page=2",
               'accept-encoding': "gzip, deflate",
               'accept-language': "zh-CN,zh;q=0.9",
               'cookie': 'UM_distinctid=165d243d684e9-0111554226bb1c-3c604504-13edd4-165d243d68516f; taihe=aebe409faefff51e20f2dde377f1cea6; ngacn0comUserInfo=%25B0%25EB%25CF%25C4%25A8q%25A5%25A1%258EU%259B%25F6%09%25E5%258D%258A%25E5%25A4%258F%25E2%2595%25AD%25E3%2582%25A1%25E5%25B6%25B6%25E6%25B6%25BC%0939%0939%09%0910%090%090%090%090%09; ngaPassportUid=43320220; ngaPassportUrlencodedUname=%25B0%25EB%25CF%25C4%25A8q%25A5%25A1%258EU%259B%25F6; ngaPassportCid=Z8ltrcjgo616kor6sbbpgr0thdnbrsr96ge8kte5; ngacn0comUserInfoCheck=10d5d900ae3f241cd4bc9d2e144794f3; ngacn0comInfoCheckTime=1537976770; taihe_session=6444150154287a3254e70831f46a8868; CNZZDATA30043604=cnzz_eid%3D364786080-1536830942-%26ntime%3D1537976642; CNZZDATA30039253=cnzz_eid%3D943882560-1536826159-%26ntime%3D1537971608; Hm_lvt_5adc78329e14807f050ce131992ae69b=1536830988,1536839697,1537976774; lastvisit=1537976828; lastpath=/read.php?tid=12689996&page=2; bbsmisccookies=%7B%22insad_refreshid%22%3A%7B0%3A%22/153794231025962%22%2C1%3A1538581572%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-46%2C1%3A1537981224%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1537981224%7D%7D; Hm_lpvt_5adc78329e14807f050ce131992ae69b=1537976834'
               }
    return headers


def down_web(url):
    retry = 5
    while True:
        try:
            text = requests.get(url, headers=get_headers()).content.decode('gbk', 'ignore')  # 读取全部网页
            return text
        except Exception as e:
            retry -= 1
            if retry == 0:
                print(e)
                return None
            else:
                continue
