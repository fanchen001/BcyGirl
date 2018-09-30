# coding=utf-8
from bcy.Stream import *
import json

#face ++ 人臉識別接口
class FacePP(object):

    def __init__(self, url):
        self.api_key ="saZmX29TUZek5vQB7NLOjI_XuwfsOsY1"
        self.api_secret = "OLsoAxqJG44Wxrh87JZsMNHFDW9vhCB4"
        self.url = url
        self.face = None
        self.body = "api_key=" + self.api_key + "&api_secret=" + self.api_secret + "&image_url=" + self.url + "&return_attributes=beauty%2Cgender%2Cskinstatus"

    #請求接口，識別圖片
    def detect(self) -> dict:
        st = Stream.url2String("https://api-cn.faceplusplus.com/facepp/v3/detect", "POST", Stream.httpHeader(self.url), self.body)
        if st is not None:
            self.face = json.loads(st)
            return self.face
        return None

    # 是否為女生
    def isGirl(self) -> bool:
        try:
            if self.face is None:
                return False
            assert isinstance(self.face, dict)
            return "Female" == self.face.get("faces")[0].get("attributes").get("gender").get("value")
        except Exception:
            pass
        return False

    #顏值打分 默認超過75為漂亮
    def isBeauty(self) -> bool:
        try:
            if self.face is None:
                return False
            assert isinstance(self.face, dict)
            beauty = self.face.get("faces")[0].get("attributes").get("beauty")
            return beauty.get("male_score") > 75 and beauty.get("female_score") > 75
        except Exception:
            pass
        return False