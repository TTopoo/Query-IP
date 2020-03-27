import requests
import json
import random
import sys
import datetime
import time
from imp import reload
import traceback


def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time():
        return int(round(time.time() * 1000))
    return current_milli_time()

reload(sys)

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'origin':'https://www.opengps.cn',
    'referer':'https://www.opengps.cn/',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}
data0={
    'random':random.random()
}
#这里的key实际上一个就够了，都是web服务的key
#key的申请地址在这儿https://lbs.amap.com/dev/key/app

key2=''
key3=''
ip=''
def getsource(ip):
#1：获取ip
    if(ip==''):
        lng=1
        lat=1
        try:
            jscontent = requests.session().post('https://www.opengps.cn/Data/IP/IPLoc.ashx',
                                                headers=head,
                                                data=data0,
                                                ).text
            jsDict = json.loads(jscontent)
            #print(jsDict)
            statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
            if statusJson == 200:
                if 'ip' in jsDict.keys():
                    ip = jsDict['ip']
                    address = jsDict['address']
                    print("Succeed:" + str(ip) + "\t" + str(address))
                else:
                    print('no data now')
            else:
                print("Error")
        except Exception as e:
            print(e)
            pass

#2：ip转经纬度
    try:
        url2='https://restapi.amap.com/v4/ip?key='+key2+'&ip='+str(ip)
        jscontent = requests.session().post(url2).text
        jsDict = json.loads(jscontent)
        #print(jsDict)
        statusJson = jsDict['errcode']
        if statusJson == 0:
            data = jsDict['data']
            pcd = data['pcd']
            lng = data['lng']
            confidence = data['confidence']
            source = data['source']
            time = data['time']
            lat = data['lat']
            print("Succeed:" + str(lng) + "\t" + str(lat))
        else:
            print(jsDict['errdetail'])
    except Exception as e:
        print(e)
        pass
#3：经纬度转地址

    try:
        url3='https://restapi.amap.com/v3/geocode/regeo?output=json&location='+str(lng)+','+str(lat)+'&key='+key3+'&radius=1000&extensions=all'
        jscontent = requests.session().post(url3).text
        jsDict = json.loads(jscontent)
        #print(jsDict)
        statusJson = jsDict['status']
        if statusJson == '1':
            
            regeocode = jsDict['regeocode']
            formatted_address = regeocode['formatted_address']
            print("Succeed: " + str(formatted_address))
        else:
            print("Error")
    except Exception as e:
        print(e)
        pass
if __name__ == "__main__":
    ip=input("请输入你的ip,留空表示本机ip,格式为 x.x.x.x：")
    getsource(ip)