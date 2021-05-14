
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


def Convert(string):
    list1=[]
    list1[:0]=string
    return list1

def Convert_2(string):
    list1= Convert(string)
    list2=[]
    #print('len',len(list1)-2)

    for i in range(0, len(list1)-1,1):
        if i%2==0:
            j = list1[i] + list1[i+1]
            #print(j)
            list2.append(j)
    return list2

def create_slots_doc(Filling_days,weekdaysno,ampmvists,SlotsAM,SlotsPM,visibility):
    slots={}
    today= datetime.date.today()


    ampmvists= Convert(ampmvists)
    SlotsAM= Convert_2(SlotsAM)
    SlotsPM= Convert_2(SlotsPM)
    #print(SlotsAM)
    #print(SlotsPM)
    #Filling_days = int(Filling_days)
    for i in  range(0,Filling_days,1):
        avdayslots={}
        nvdayslots={}
        avdayslots['visibility'] = visibility
        nvdayslots['visibility'] = visibility

        weekday = today.weekday() + 1
        weekdaysno= Convert(weekdaysno)
        date_time = today.strftime("%d/%m/%Y")
        #print("Weekday",weekday, "weekdaysno",weekdaysno,"date and time:",date_time)
        if str(weekday) in  weekdaysno:
            ind= weekdaysno.index(str(weekday))
            #print('ind',ind)
            if ampmvists[ind]=='b':
                avdayslots['am']=int(SlotsAM[ind])
                avdayslots['pm']=int(SlotsPM[ind])

            elif ampmvists[ind]=='a':
                avdayslots['am']=int(SlotsAM[ind])
                avdayslots['pm']=0
            elif ampmvists[ind]=='p':
                avdayslots['pm']=int(SlotsPM[ind])
                avdayslots['am']=0
            else:
                pass
            #avdayslots['date']=date_time
            slots[date_time]= avdayslots

        #    print("FOUND Weekday",weekday, "weekdaysno",weekdaysno,"date and time:",date_time)
        else:
            nvdayslots['am']=0
            nvdayslots['pm']=0
            #nvdayslots['date']=date_time
            slots[date_time]= nvdayslots

        today = today + datetime.timedelta(days=+1)
    print("Slots",slots)
    return slots
