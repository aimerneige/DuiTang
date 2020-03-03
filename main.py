#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author:  AimerNeige

from urllib.request import urlretrieve
import requests
import json
# import time
# import re
import os

def getPicturesBySearch(keyword:'str', limit:'int', start:'int') -> 'str':
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

def getPicturesByAlbum(album_id:'str', limit:'int', start:'int') -> 'str':
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
        urlretrieve(url, filePath, reporthook = reporthook)
        print("下载完成！")
    else:
        print("该目录下已经存在了同名文件！下载失败！")
    filesize = os.path.getsize(filePath)
    print("文件名：%s" % name)
    print("文件大小：%.2f Mb" % (filesize/1024/1024))




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
    nextStart = data['next_start'] # 下一页的索引
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