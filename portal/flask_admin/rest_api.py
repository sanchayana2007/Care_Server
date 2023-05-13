import requests
import json
import configparser
parser = configparser.ConfigParser()
parser.read('serverconfig.ini')
api = 'booking/slotadd' 


headers1 = {'Authorization':'Bearer ' + parser['Authorisation']['Authorization'], 'x-Origin-Key': parser['Headers']['x-Origin-Key'],'x-Api-Key': parser['Headers']['x-Api-Key'], 'content-type' : parser['Headers']['content-type'], 'charset': parser['Headers']['charset']}

body= {'aid' : 1,'did' : '608bc4507b40eb6803659557','cid' : '608793ae5c88f3bdb38d6530','date': '17/05/2021'}

def get_call(api,body):
    r = requests.get(parser['server_link']['rest_api']+ api,data=json.dumps(body), headers=headers1) 
    return json.loads(r.content)

def post_call(api,body):
    r = requests.post(parser['server_link']['rest_api']+ api,data=json.dumps(body), headers=headers1) 
    return json.loads(r.content)

def put_call(api,body):
    r = requests.put(parser['server_link']['rest_api']+ api,data=json.dumps(body), headers=headers1) 
    return json.loads(r.content)

def del_call(api,body):
    r = requests.delete(parser['server_link']['rest_api']+ api,data=json.dumps(body), headers=headers1) 
    return json.loads(r.content)
