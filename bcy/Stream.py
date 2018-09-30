# coding=utf-8

from urllib.request import Request
from urllib.request import urlopen
from http.client import HTTPResponse
import gzip
import zlib
import os

#流相關操作
class Stream(object):

    #默認http請求頭
    @classmethod
    def httpHeader(cls, referer="", mobile=False) -> {}:
        if not mobile:
            agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
        else:
            agent = "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Mobile Safari/537.36"
        return {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "User-Agent": agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": referer,
            "Upgrade-Insecure-Requests": "1",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "PHPSESSID=96fb7956371235cc94b2356be4c4c344; lang_set=zh; mobile_set=no; _ga=GA1.2.56893931.1538128347; _gid=GA1.2.415574804.1538128347; Hm_lvt_330d168f9714e3aa16c5661e62c00232=1538128350; __tea_sdk__ssid=f133c75c-81aa-45a3-9b30-2025ca0f1e54; tt_webid=6606210957503923725; __tea_sdk__user_unique_id=6606210957503923725; _csrf_token=6d5978bd39433c212e1119a06a56f283; Hm_lpvt_330d168f9714e3aa16c5661e62c00232=1538128495"
        }

    # url2String
    @classmethod
    def url2String(cls, url, method="GET", header=None, data=None, encode="UTF-8") -> str:
        byte = Stream.url2Byte(url, method, header, data)
        if byte is not None:
            return str(byte, encode)
        return None

    # url2Byte
    @classmethod
    def url2Byte(cls, url, method="GET", header={}, data=None) -> bytes:
        conn = None
        byte = None
        try:
            if header is not None:
                if data is not None:
                    if isinstance(data, str):
                        data = data.encode("UTF-8")
                req = Request(url, data=data, headers=header, method=method)
                conn = urlopen(req)
            else:
                conn = urlopen(url)
            if conn.getcode() == 200:
                assert isinstance(conn, HTTPResponse)
                head = conn.getheader("Content-Encoding")
                if "gzip" == head:
                    byte = Stream.deGzip(conn.read())
                elif "deflate" == head:
                    byte = Stream.deDeflate(conn.read())
                else:
                    byte = conn.read()
        except Exception as err:
            err.with_traceback()
            return None
        finally:
            if conn is not None:
                conn.close()
        return byte

    # gzip解壓
    @classmethod
    def deGzip(cls, data) -> bytes:
        try:
            return gzip.decompress(data)
        except Exception:
            return None

    # deflate解壓
    @classmethod
    def deDeflate(cls, data) -> bytes:
        try:
            return zlib.decompress(data, -zlib.MAX_WBITS)
        except zlib.error:
            try:
                return zlib.decompress(data)
            except zlib.error:
                return None

    # byte2File
    @classmethod
    def byte2File(cls, byte, file) -> bool:
        if byte is None or file is None:
            return False
        f = None
        try:
            f = open(file, "wb+")
            f.write(byte)
            return True
        except Exception:
            pass
        finally:
            if f is not None:
                f.close()
        return False

    #創建文件夾
    @classmethod
    def mkDir(cls, path) -> bool:
        if path is None:
            return False
        assert isinstance(path, str)
        path.strip()
        if os.path.exists(path):
            return False
        os.makedirs(path)
        return True
