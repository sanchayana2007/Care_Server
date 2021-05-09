
from .conn_util import MongoMixin
from .build_config import *

#User profile to identify the App



async def validate_profile(entityId,accountId,applicationId):
    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]
    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]
    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]
    profileQ =  profile.find(
            {
                'closed': False,
                'entityId':  entityId,
                'accountId':  accountId,
                'applicationId':  applicationId
            },
            {
                '_id': 1
            },
            limit=1
        )
    profile = []
    async for i in profileQ:
        profile.append(i)

    if len(profile):
        profileId = profile[0]['_id']
        Log.i('ProfID',  profileId)
        appQ =  applications.find(
                {
                    '_id':  applicationId
                },
                {
                    '_id': 1,
                    'apiId': 1
                },
                limit=1
        )
        app = []
        async for i in appQ:
                app.append(i)
        #print("COOMON_UTIL",app)
    return int(app[0]['apiId'])
