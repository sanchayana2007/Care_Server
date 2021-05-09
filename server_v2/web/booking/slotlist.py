#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    1.  DocterListHandler
        Type: Class
        Methods:
            A.GET:
                Get all doctor  details under that entity
                Line: 39
            B.POST:
                Will create new row doctors
                Line: 162
            C.PUT:
                Update Doctor details on doctors.
                Line: 335
            D:DELETE:
                Delete the Doctor from list.
                Line: 523
'''

from __future__ import division
from PIL import Image
from ..lib.lib import *
import requests
import http.client
import datetime

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




@xenSecureV1
class SlotListHandler(tornado.web.RequestHandler):

    SUPPORTED_METHODS = ('GET','POST','PUT','DELETE')

    #User profile to identify the App
    profile = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][2]['name']
                ]
    account = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][0]['name']
                ]
    applications = MongoMixin.userDb[
                    CONFIG['database'][0]['table'][1]['name']
                ]
    #Other Item lists
    doc_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][0]['name']
                ]
    clinic_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][1]['name']
                ]
    slot_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][2]['name']
                ]

    fu = FileUtil()
    #Post is admin run for 30 days pre polpulate slots
    async def post(self):

        status = False
        code = 4000
        result = []
        message = ''
        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            Log.i('entityId', self.entityId)
            Log.i('accountId', self.accountId)
            Log.i('applicationId', self.applicationId)
            profileQ = self.profile.find(
                    {
                        'closed': False,
                        'entityId': self.entityId,
                        'accountId': self.accountId,
                        'applicationId': self.applicationId
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
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                        {
                            '_id': self.applicationId
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

                if len(app):
                    self.apiId = app[0]['apiId']
                    if self.apiId in [ 502020, 502022]:
                        #Doc Clinic App doc addition req handling
                        if self.apiId == 502020:

                            try:
                                #Mandatory the field Validation needs to be checked by APP

                                slotDate  = datetime.date.today()
                                #slotDateOffset = self.request.arguments.get('slotdateoffset')
                                slotDateOffset = 10
                                #All records from
                                docID = None
                                clinicId = None #App populated
                                paymentID = None
                                totalSlots = self.request.arguments.get('starttime')
                                availableSlots = self.request.arguments.get('endtime')
                                Log.i('slotDate', slotDate)
                            except:
                                code = 4888
                                message = "Invalid Request Body "
                                raise Exception
                            #Get all the records from the doctor list
                            docQ = self.doc_list.find(
                                            {

                                            },
                                            {
                                                'docname':1,
                                                'doclocation':1,
                                                'speciality':1,
                                                'clinicid':1,
                                                'days':1,
                                                'totalslotsam':1,
                                                'totalslotspm':1,
                                                'ampmvists' : 1,
                                                'doccomment':1,
                                                'docratings':1,
                                                'totalpatients':1

                                            }
                                        )

                            docdetails = []
                            slotdetails=[]
                            async for i in docQ:
                                docdetails.append(i)
                            Log.i("docdetails",docdetails)
                            if  len(docdetails):
                                    for doc in docdetails:
                                        Log.i("clinicid",str(doc['clinicid']))
                                        clinicId = doc['clinicid']

                                        clinicQ = self.clinic_list.find(
                                                        {
                                                            '_id': clinicId
                                                        },
                                                            {
                                                                'clinicname':1,
                                                                'cliniclocation': 1,
                                                                'clinicaddress': 1,
                                                                'pocclinicph': 1,
                                                                'paymentadd': 1,
                                                                'clinicpaymentaddress': 1,
                                                                'comment':"Entry test "
                                                            },
                                                            limit=1
                                                    )
                                        clinicdetails=[]
                                        async for i in clinicQ:
                                            clinicdetails.append(i)
                                        if len(clinicdetails):

                                            monthly_slots={}
                                            weekdays = doc['days']
                                            totalslots=10
                                            ampmvists = doc['ampmvists']
                                            totalSlotsAM= doc['totalslotsam']
                                            totalSlotsPM= doc['totalslotspm']
                                            visibility = True
                                            monthly_slots['monthly_slots']= create_slots_doc(totalslots,weekdays,ampmvists,totalSlotsAM,totalSlotsPM,visibility)
                                            #Log.i("monthly_slots",monthly_slots)
                                            doc['doc_id']= str(doc['_id'])
                                            del doc['_id']
                                            clinicdetails[0]['clinic_id']= str(clinicdetails[0]['_id'])
                                            del clinicdetails[0]['_id']

                                            del doc['clinicid']
                                            #Log.i("Adoc",doc)
                                            #Log.i("Aclinicdetails",clinicdetails[0])
                                            slotitm =  {**doc,**clinicdetails[0],**monthly_slots}
                                            #Log.i("slotitm",slotitm)
                                            slotdetails.append(slotitm)
                                            Log.i("slotdetails",slotdetails)
                                        else:
                                            message = "NoClinic id is found with doc details "
                                            raise Exception




                                    #Enter the slot details in teh slot list table
                                    for i in slotdetails:
                                        slotQ = self.slot_list.find(
                                                        {
                                                            'doc_id':str(i['doc_id']),

                                                        },
                                                        {
                                                            'docname':1,
                                                            'doclocation':1,
                                                            'speciality':1,
                                                            'clinicid':1
                                                        }
                                                    )
                                        slotdetails = []
                                        async for i in slotQ:
                                            slotdetails.append(i)
                                            Log.i('slot indb',i)


                                        if  len(slotdetails):
                                            code= 4055
                                            status = False
                                            message = "Doc slot  Already Found"
                                            Log.i('Doc Already found  Account', docdetails)
                                            raise Exception







                                        SlotId = self.slot_list.insert_one(i.copy())





                                        if SlotId:
                                            Log.i("SlotId inserted",SlotId)
                                            code = 2000
                                            message = "SlotId is has been added"
                                            status = True
                                        else:
                                            Log.i("SlotId not inserted")
                                            code = 2000
                                            message = "Error in SlotId addition"
                                            status = True

                            else:
                                message = "No Doc id is found cant book slots"
                                raise Exception


                            #for each items in the doc list insert one
                            #
                            # as a dictionary [date]= Avialabe slots for the doctor
                            # loop to create it for 10 days

                elif self.apiId == 502022:
                            try:
                                docId = ObjectId(self.request.arguments.get('docId'))
                            except:
                                code = 4888
                                message = "Invalid Booking Id"
                                raise Exception

                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not Authorized.'


        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return
    #To insert the Doctor data nd
    async def put(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            areaId = int(self.request.arguments["aid"])
            docId = str(self.request.arguments["did"])
            clinicId = str(self.request.arguments["cid"])
            try :
                seldate=  str(self.request.arguments["date"])
            except:
                seldate= None
            Log.i("areaId",areaId)
            Log.i("docId",docId)
            Log.i("clinicId",clinicId)
            Log.i("seldate",seldate)


            self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)
                #Determine which app has sent it
            if self.apiId:
                Log.i(self.apiId)
                #TODO : Change ths code to 502022
                if self.apiId == 502020:
                    Log.i('Clinic PUT req', self.request.arguments)
                    result=[]
                    if docId != None and clinicId != None and seldate != None:

                        Log.i(seldate)
                        slots  = await self.slot_list.find_one(
                                {
                                    "clinic_id":  clinicId,
                                    "doc_id" : docId
                                }
                            )
                        #Res is from clinic_list collections whatevr matches
                        if slots:
                            Log.i('seldate data',slots['monthly_slots'][seldate])
                            Log.i('visibility',slots['monthly_slots'][seldate]['visibility'])
                            resDoc = await self.slot_list.update_one(
                                    {
                                        "clinic_id":  clinicId,
                                        "doc_id" : docId,
                                        'monthly_slots.'+ seldate + '.am' : {'$gt': 0}
                                    },
                                    {
                                    '$inc':{
                                                'monthly_slots.'+ seldate + '.am' : -1
                                           }
                                    }
                                )
                            code = 2000
                            status = True
                            message = "Doctors Found in Clinic"
                        else:
                            code = 4080
                            status = False
                            message = "No data found"






                        Log.i("datestr",type(resDoc))
                        Log.i("datestr", resDoc.modified_count)

                    '''
                    phoneNumber = serBook[0]['accountDetails'][0]['contact'][0]['value']
                    # TODO: Country code hard coded
                    phoneNumber = str(phoneNumber - 910000000000)
                    Log.i('Customer Phone Number', phoneNumber)

                    serListQ = self.serviceList.find(
                                {
                                    '_id':serBook[0]['serviceId']
                                }
                            )
                    serList = []
                    async for i in serListQ:
                        serList.append(i)
                    if not len(serList):
                        code = 4060
                        message = "Invalid Service"
                        raise Exception

                    serName = serList[0]['serNameEnglish']

                    if stage in ['accepted','declined','completed','declined_fee']:
                        serUpdate = self.doc_list.update_one(
                                    {
                                        '_id':docId
                                    },
                                    {
                                    '$set':{
                                                'stage':stage
                                           }
                                    }
                                )
                    '''
                elif self.apiId == 502022:
                    try:
                        docId = ObjectId(self.request.arguments.get('docId'))
                    except:
                        code = 4050
                        message = "Invalid Booking Id"
                        raise Exception
                    serBookQ = self.doc_list.find(
                                {
                                    '_id':docId
                                }
                            )
                    serBook = []
                    async for i in serBookQ:
                        serBook.append(i)
                    if not len(serBook):
                        code = 4060
                        message = "Invalid Booking"
                        raise Exception
                    phoneNumber = serBook[0]['accountDetails'][0]['contact'][0]['value']
                    # TODO: Country code hard coded
                    phoneNumber = str(phoneNumber - 910000000000)
                    Log.i('Customer Phone Number', phoneNumber)

                    serListQ = self.serviceList.find(
                                {
                                    '_id':serBook[0]['serviceId']
                                }
                            )
                    serList = []
                    async for i in serListQ:
                        serList.append(i)
                    if not len(serList):
                        code = 4060
                        message = "Invalid Service"
                        raise Exception

                    serName = serList[0]['serNameEnglish']

                    serUpdate = self.doc_list.update_one(
                                {
                                    '_id':docId
                                },
                                {
                                '$set':{
                                            'stage':'declined'
                                        }
                                }
                            )
                    sms = 'Greetings from Ohzas! We are sorry to know that you \
                            have cancelled the appointment for {}. \
                            We look forward to provide service to you again.'.format(serName)
                    if serUpdate['n']:
                        conn = http.client.HTTPSConnection("api.msg91.com")
                        payloadJson = {
                                        "sender":"SOCKET",
                                        "route":4,
                                        "country":91,
                                        "sms":[
                                                {
                                                    "message":sms,
                                                    "to":[phoneNumber]
                                                }
                                            ]
                                        }
                        payload = json.dumps(payloadJson)
                        headers = {
                                    'authkey': MSG91_GW_ID,
                                    'content-type': "application/json"
                                }
                        conn.request("POST", "/api/v2/sendsms", payload, headers)
                        res = conn.getresponse()
                        data = res.read()
                        stat = json.loads(data.decode("utf-8"))
                        Log.i('Notification Status',stat['type'])

                        if stat['type'] == "success":
                            code = 2000
                            message = "Request has been cancelled"
                            status = True
                        else:
                            code = 4055
                            Log.i('SMS notification could not be sent')
                    else:
                        code = 2000
                        message = "Invalid booking"
                        status = True
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not Authorized.'
            else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not Authorized.'


        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                Log.w('EXC', iMessage)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return

    async def get(self):

        status = False
        code = 4000
        result = []
        message = ''

        self.request.arguments =  json.loads(self.request.body.decode('utf-8'))

        areaId = int(self.request.arguments["aid"])
        docId = str(self.request.arguments["did"])
        clinicId = str(self.request.arguments["cid"])
        try :
            seldate=  str(self.request.arguments["date"])
        except:
            seldate= None
        Log.i("areaId",areaId)
        Log.i("docId",docId)
        Log.i("clinicId",clinicId)

        Log.i("seldate",seldate)


        try:
            # TODO: this need to be moved in a global class
            self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)
                #Determine which app has sent it
            if self.apiId:

                if self.apiId in [ 502020, 502022]: # TODO: till here
                    #Handle the Clinic Doc list get request
                    #Show only the listed doctor for that clinic
                    if self.apiId == 502022:
                        resQ = self.slot_list.find(
                                {
                                    'doc_id': docId,
                                    'clinic_id': clinicId
                                }
                            )
                        res = []
                        async for i in resQ:
                            res.append(i)
                        #Res is from clinic_list collections whatevr matches
                        if len(res):
                            Log.i('res',res)
                            for i in res:
                                i["_id"]= str(i["_id"])
                                result.append(i)
                            result.reverse()
                            code = 2000
                            status = True
                            message = "Doctors Found in Clinic"
                        else:
                            code = 4080
                            status = False
                            message = "No data found"

                    #Patient App Handling
                    elif self.apiId == 502020:
                        result = []
                        Log.i("docid object",docId)
                        Log.i("clinicid object",clinicId)
                        #Doc and clinic both are None show all Docs in all clinics
                        if docId != None and clinicId != None and seldate == None:
                            resDoc = self.slot_list.find(
                                    {
                                        "clinic_id":  clinicId,
                                        "doc_id" : docId
                                    }
                                )
                            async for i in resDoc:
                                i["_id"]= str(i["_id"])
                                result.append(i)

                        elif docId != None and clinicId != None and seldate != None:
                            datestr="monthly_slots."+ seldate
                            Log.i(datestr)
                            resDoc = self.slot_list.find(
                                    {
                                        "clinic_id":  clinicId,
                                        "doc_id" : docId
                                    }

                                )
                            async for i in resDoc:
                                i["_id"]= str(i["_id"])
                                datedata= i["monthly_slots"][seldate]

                                result.append(datedata)
                            Log.i("datestr",datedata)

                        else:
                            pass

                        Log.i("Result",result)


                        #Create the response
                        if len(result):
                            result.reverse()
                            code = 2000
                            status = True
                            message = "Doc List Found "
                        else:
                            code = 4080
                            status = False
                            message = "No data found"
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not authorized.'

        except Exception as e:
            status = False
            result = []
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            result = []
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return


    async def delete(self):

        status = False
        code = 4000
        result = []
        message = ''

        try:
            try:
                # CONVERTS BODY INTO JSON
                docId = ObjectId(self.request.arguments['id'][0].decode())
            except Exception as e:
                code = 4100
                message = 'Invalid ID'
                raise Exception
            # TODO: this need to be moved in a global class, from here
            profileQ = self.profile.find(
                    {
                        'closed': False,
                        'entityId': self.entityId,
                        'accountId': self.accountId,
                        'applicationId': self.applicationId
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
                self.profileId = profile[0]['_id']
                Log.i('PID', self.profileId)
                appQ = self.applications.find(
                        {
                            '_id': self.applicationId
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

                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] == 502022:# TODO: till here
                        bookDel = self.doc_list.update_one(
                                    {
                                        '_id':docId
                                    },
                                    {
                                    '$set':{
                                            'disabled':True
                                           }
                                    }
                                )
                        if bookDel['n']:
                            code = 2000
                            status = True
                            message = "Booking entry has been removed from active entries"
                        else:
                            code = 4210
                            status = False
                            message = 'This entry does not exist.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not authorized.'
                else:
                    code = 4003
                    self.set_status(401)
                    message = 'You are not authorized.'
            else:
                code = 4003
                self.set_status(401)
                message = 'You are not authorized.'

        except Exception as e:
            status = False
            #self.set_status(400)
            if not len(message):
                template = 'Exception: {0}. Argument: {1!r}'
                code = 5010
                iMessage = template.format(type(e).__name__, e.args)
                message = 'Internal Error Please Contact the Support Team.'
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = exc_tb.tb_frame.f_code.co_filename
                Log.w('EXC', iMessage)
                Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
        response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
        Log.d('RSP', response)
        try:
            response['result'] = result
            self.write(response)
            self.finish()
            return
        except Exception as e:
            status = False
            template = 'Exception: {0}. Argument: {1!r}'
            code = 5011
            iMessage = template.format(type(e).__name__, e.args)
            message = 'Internal Error Please Contact the Support Team.'
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            Log.w('EXC', iMessage)
            Log.d('EX2', 'FILE: ' + str(fname) + ' LINE: ' + str(exc_tb.tb_lineno) + ' TYPE: ' + str(exc_type))
            response =  {
                    'code': code,
                    'status': status,
                    'message': message
                }
            self.write(response)
            self.finish()
            return
