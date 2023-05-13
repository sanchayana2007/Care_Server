
from .conn_util import MongoMixin
from .build_config import *
from datetime import date,datetime,timedelta
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
    else:
        Log.i('ProfID is not found')
        return 0


def create_slots_doc(slottotaldays,slotData):
    slots={}
    today= date.today()
    
    
    for i in  range(0,slottotaldays,1):
                
        weekday = datetime.weekday(today)
        #date_time = datetime.strftime("%d/%m/%Y")
        date_time = today.strftime("%d/%m/%Y")
        #print("Weekday",weekday, "date and time:",date_time, slotData[weekday])
        
        if slotData[weekday]:
            slotData[weekday]['AvSlotsAM'] = slotData[weekday]['totalSlotsAM']- 1
            slotData[weekday]['AvSlotsPM'] = slotData[weekday]['totalSlotsPM'] -1
            slotData[weekday]['Visibility'] = False
            slots[date_time]= slotData[weekday]
        else:
            print(str(slotData[weekday])+ "Is not a valid weekday")
           
        today = today +  timedelta(days=+1)


    #print("Slots",slots)
    return slots

def Av_weekdays(slotData):
    Av_days = []
    weeklist= ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    for i in  range(0,7):
        if  slotData[i]['totalSlotsPM'] > 0 or slotData[i]['totalSlotsPM'] > 0 :
            Av_days.append(weeklist[i])
    return Av_days
        


def create_slots_list(slotData , no_of_days=30):
    slots= []
    today= date.today()
    
    print("create_slots_list")
    for i in  range(0,no_of_days,1):
        date_time = today.strftime("%d/%m/%Y")
        print("date and time:",date_time )
        
        if date_time in  slotData:
            #slots.append({date_time : slotData[date_time]})
            newdict = {}
            newdict = slotData[date_time].copy()
            newdict.update({'date':date_time})
            slots.append(newdict)
        else:
            print(date_time + "Not found in slot data")
           
        today = today +  timedelta(days=+1)


    print(" listed slots Slots",slots)
    return slots