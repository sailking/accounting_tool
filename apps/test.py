import json, requests
from pprint import pprint
def search_package():
    package_number = "YG1681082237738DE"
    com_autoauth_url = "https://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={}".format(package_number)
    response_data = json.loads(requests.get(com_autoauth_url).text)
    com_name = response_data["auto"][0]["comCode"]
    
    search_url = "https://www.kuaidi100.com/query?type={}&postid={}".format(com_name, package_number)
    package_info = json.loads(requests.get(search_url).text)
    pprint(package_info)
    print("快递信息：")
    print("时间                    地点和跟踪进度")
    
    for item in package_info['data']:
        print(item['ftime'], item['context'])
    
    
search_package()