#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  AimerNeige

from urllib.request import urlretrieve
import requests
import json
import re
import os

'''
需要下载的库
requests
'''

rootPath = '/home/aimerneige/spider/duitang/'

def getJsonBySearch(keyword:'str', limit:'int', start:'int') -> 'str':
    """
    通过关键词搜索获取图片的json数据
    :param keyword: 搜索关键词
    :param limit:   返回数据数量限制（最大为100，使用大于100的数据会按照100处理）
    :param start:   从何处开始访问数据（索引）
    :return str:    json数据
    """
    url = "https://www.duitang.com/napi/blog/list/by_search/?kw=%s&type=feed&limit=%d&start=%d" % (keyword, limit, start)
    response = requests.get(url)
    if response.status_code != 200:
        print("Request failed!")
        return
    response.encoding = 'utf-8'
    jsonData = response.text
    return jsonData

def getJsonByAlbum(album_id:'str', limit:'int', start:'int') -> 'str':
    """
    通过专辑id获取图片的json数据
    :param album_id:专辑id
    :param limit:   返回数据数量限制（最大为100，使用大于100的数据会按照100处理）
    :param start:   从何处开始访问数据（索引）
    :return str:    json数据
    """
    url = "https://www.duitang.com/napi/blog/list/by_album/?album_id=%s&limit=%d&start=%d" % (album_id, limit, start)
    response = requests.get(url)
    if response.status_code != 200:
        print("Request failed!")
        return
    response.encoding = 'utf-8'
    jsonData = response.text
    return jsonData

def download(url, path, name):
    """
    下载文件
    :param url: 文件链接
    :param path: 保存目录
    :param name: 文件名称
    :return: None
    """
    def reporthook(a, b, c):
        """
        显示下载进度
        :param a: 已经下载的数据块
        :param b: 数据块的大小
        :param c: 远程文件大小
        :return: None
        """
        print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="")

    filePath = os.path.join(path, name)
    if not os.path.isfile(filePath):
        print("开始下载：%s" % url)
        print("文件名：%s" % name)
        urlretrieve(url, filePath, reporthook = reporthook)
        print("下载完成！")
    else:
        print("该目录下已经存在了同名文件！下载失败！")
    filesize = os.path.getsize(filePath)
    print("文件大小：%.2f Mb" % (filesize/1024/1024))

def spider(value:'str', getAll:'str', minSize:'int', withId:'str'):
    allFlag = False
    if (getAll == "y" or getAll == "Y" or getAll == "yes" or getAll == "Yes"):
        allFlag = True
    if allFlag:
        limit = 100
    else:
        limit = input("你想要每次爬取多少张图片？（最大100）\n")
    next_start = 0
    while True:
        idFlag = False
        if (withId == "y"):
            idFlag = True
        if idFlag:
            jsonData = getJsonByAlbum(value, limit, next_start)
        else:
            jsonData = getJsonBySearch(value, limit, next_start)
        jsonItem = json.loads(jsonData)
        if jsonItem['status'] != 1:
            print("无法获取数据！这些信息可能会帮到你：\n%s" % jsonItem)
            exit()
        else:
            data = jsonItem['data']
            next_start = data['next_start']
            objectList = data['object_list']
            for objectItem in objectList:
                photo = objectItem['photo']
                size = int(photo['size'])
                if (size < minSize):
                    continue
                url = photo['path']
                picId = objectItem['id']
                nameEnd = re.findall(r'.*_(.*)', url)[0]
                name = "%s_%s" % (picId, nameEnd)
                # if not os.path.exists(rootPath):
                #     os.makedirs(rootPath)
                newPath = os.path.join(rootPath, "%s/" % value)
                if not os.path.exists(newPath):
                    os.makedirs(newPath)
                download(url, newPath, name)
            more = data['more']
            if more != 1:
                print("已经没有更多图片了！")
                break
            if not allFlag:
                a = ("还要继续爬吗 Y/N\n")
                if (a == "y" or a == "Y" or a == "yes" or a == "Yes"):
                    continue
                else:
                    break

def main():
    print("欢迎来到堆糖爬虫！作者：AimerNeige")
    print("仅供个人学习使用，请勿用于非法用途！")
    print("当前保存目录为%s，如果需要修改请修改源码" % rootPath)
    print("请选择爬取类型")
    print("1. 通过关键词爬取\t\t爬取关键词搜索结果")
    print("2. 通过专辑id爬取\t\t爬取专辑的所有图片")
    status_way = input()
    withId = 'y'
    value = "miku"
    getAll = 'y'
    if status_way == "1":
        withId = 'n'
        value = input("请输入搜索关键词\n")
    elif status_way == "2":
        value = input("请输入专辑Id（url里面有）\n")
    else:
        print("输入有误，请重新输入。")
        main()
    getAll = input("是否自动爬取全部图片 Y/N\n")
    minSize = int(input("被过滤图片的大小，小于该数值则不会下载（整数、单位kb）\n"))
    minSize = minSize * 1024
    spider(value, getAll, minSize, withId)

main()

'''
def jsonParse(jsonData):
    """
    json数据使用示例，仅解释核心有用数据
    :param jsonData: json数据
    :return: None
    """
    jsonData = getPicturesByAlbum("86215915", 12, 0)
    jsonItem = json.loads(jsonData)
    print(jsonItem)
    status = jsonItem['status'] # 状态码：1 正常，4 错误，会返回错误提示
    print(status)
    data = jsonItem['data'] # 数据
    print(data)
    nextStart = data['next_start'] # 下一页的索引nex
    print(nextStart)
    objectList = data['object_list'] # 数据列表
    print(objectList)
    objectItem = objectList[0] # 数据列表元素
    print(objectItem)
    photo = objectItem['photo'] # 图片信息
    print(photo)
    width = photo['width'] # 宽
    print(width)
    height = photo['height'] # 高
    print(height)
    path = photo['path'] # 图片地址
    print(path)
    size = photo['size'] # 图片大小，以字节为单位
    print(size)
    msg = objectItem['msg'] # 图片附带信息
    print(msg)
    id = objectItem['id'] # id
    print(id)
    more = data['more'] # 是否有更多内容（是否有下一页）
    print(more)
    limit = data['limit'] # 返回数量限制
    print(limit)

jsonData = getPicturesByAlbum("86215915", 12, 0)
jsonParse(jsonData)

"""
返回数据示例
{
    "status": 1,
    "data": {
        "total": 183,
        "next_start": 12,
        "object_list": [
            {
                "photo": {
                    "width": 1067,
                    "height": 1500,
                    "path": "https://c-ssl.duitang.com/uploads/item/201910/02/20191002074225_pvols.jpg",
                    "size": 318658
                },
                "msg": "P站--hiten",
                "id": 1137325349,
                "buyable": 0,
                "source_link": "",
                "add_datetime": "2019年10月2日 7:42",
                "add_datetime_pretty": "5个月前",
                "add_datetime_ts": 1569973351,
                "icon_url": "",
                "sender_id": 15970376,
                "favorit# jsonData = getPicturesByAlbum("86215915", 12, 0)ify_user": false
            }
        ],
        "more": 1,
        "limit": 12
    }
}
"""
'''