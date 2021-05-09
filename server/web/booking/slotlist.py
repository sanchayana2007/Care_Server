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

def create_slots_doc(Filling_days,weekdaysno,ampmvists,SlotsAM,SlotsPM,):
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
        weekday = today.weekday() + 1
        weekdaysno= Convert(weekdaysno)
        date_time = today.strftime("%d/%m/%Y")
        #print("Weekday",weekday, "weekdaysno",weekdaysno,"date and time:",date_time)
        if str(weekday) in  weekdaysno:
            ind= weekdaysno.index(str(weekday))
            #print('ind',ind)
            if ampmvists[ind]=='b':
                avdayslots['am']=SlotsAM[ind]
                avdayslots['pm']=SlotsPM[ind]

            elif ampmvists[ind]=='a':
                avdayslots['am']=SlotsAM[ind]
                avdayslots['pm']=00
            elif ampmvists[ind]=='p':
                avdayslots['pm']=SlotsPM[ind]
                avdayslots['am']=00
            else:
                pass
            slots[date_time]= avdayslots
        #    print("FOUND Weekday",weekday, "weekdaysno",weekdaysno,"date and time:",date_time)
        else:
            nvdayslots['am']=None
            nvdayslots['pm']=None
            slots[date_time]= nvdayslots
        today = today + datetime.timedelta(days=+1)

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

                                            monthly_slots['monthly_slots']= create_slots_doc(totalslots,weekdays,ampmvists,totalSlotsAM,totalSlotsPM)
                                            #Log.i("monthly_slots",monthly_slots)
                                            del doc['_id']
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
                                                            'docname':i['docname'],
                                                            'doclocation': i['doclocation'],
                                                            'speciality':  i['doclocation'],
                                                            'clinicname': i['clinicname']
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



                            '''
                            try:
                                serviceId = ObjectId(self.request.arguments.get('serviceId'))
                            except:
                                code = 4888
                                message = "Invalid Service Id"
                                raise Exception

                            try:
                                aTime = long(self.request.arguments.get('time'))
                                code, message = Validate.i(
                                         aTime,
                                         'Time',
                                        )
                                if code != 4100:
                                    raise Exception
                            except Exception as e:
                                code = 4210
                                message = 'Invalid Argument - [ time ].'
                                raise Exception


                            comment = self.request.arguments.get('comment')
                            code, message = Validate.i(
                                            comment,
                                            'Comment',
                                            dataType=unicode,
                                            maxLength=400
                                        )
                            if code != 4100:
                                raise Exception

                            session = self.request.arguments.get('session')
                            if session == None or session == 'One-time-session':
                                session = 1
                            else:
                                code, message = Validate.i(
                                                session,
                                                'session',
                                                datatype=int,
                                            )
                                if code != 4100:
                                    raise Exception

                            accDetailsQ = self.account.find(
                                            {
                                                '_id':self.accountId,
                                            },
                                            {
                                                '_id':0,
                                                'firstName':1,
                                                'lastName':1,
                                                'contact':1
                                            }
                                        )
                            accDetails = []
                            async for i in accDetailsQ:
                                accDetails.append(i)

                            if not len(accDetails):
                                code= 4055
                                status = False
                                message = "No Account Found"
                                raise Exception

                            fullName = str(accDetails[0]['firstName']) + ' ' + str(accDetails[0]['lastName'])
                            phoneNumber = accDetails[0]['contact'][0]['value']
                            # TODO: Country code hard coded
                            phoneNumber = str(phoneNumber - 910000000000)
                            Log.i('Customer Phone Number', phoneNumber)


                            serListQ = self.serviceList.find(
                                        {
                                            '_id':serviceId
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

                            cancelFeeQQ = self.cancelFee.find(
                                            {
                                                'profileId':self.profileId
                                            }
                                        )
                            cancelFeeQ = []
                            async for i in cancelFeeQQ:
                                cancelFeeQ.append(i)
                            if len(cancelFeeQ):
                                cancelFeeAmt = cancelFeeQ[0]['cancellationFee']
                            else:
                                cancelFeeAmt = 0

                            docId = self.doc_list.insert_one(
                                        {
                                            'disabled':False,
                                            'cancelFee':cancelFeeAmt,
                                            'accountDetails':accDetails,
                                            'stage':'new',
                                            'serviceId':serviceId,
                                            'booktime':aTime,
                                            'session':session,
                                            'session_remaining':session,
                                            'requestedTime':timeNow(),
                                            'profileId':self.profileId,
                                            'entityId':self.entityId,
                                            'comment':comment
                                        }
                                    )

                            date = int(aTime/1000000)
                            date = date + 19800
                            newDate = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %I:%M:%p')

                            if docId:
                                cancelFeeDel = self.cancelFee.delete_many(
                                                {
                                                    'profileId':self.profileId
                                                }
                                            )
                                conn = http.client.HTTPSConnection("api.msg91.com")
                                sms = 'Greetings from Ohzas. Your appointement for {} at {} has been \
                                        placed on request'.format(serName,newDate)
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
                                    message = "Request has been submitted."
                                    Log.i('SMS notification is sent')
                                    status = True
                                else:
                                    code = 4055
                                    message = "Request has been submitted."
                                    Log.i('SMS notification could not be sent')
                                    status = True
                                sms = 'Hi! A Request to appointement for {} at {} has been \
                                        placed through the OHZAS app. The request is placed by \
                                        {} and the contact number is {}'\
                                        .format(serName,newDate,fullName,phoneNumber,)
                                adminNum = str(CONFIG['medAdmin_contact'][0]['num1'])
                                payloadJson = {
                                                "sender":"SOCKET",
                                                "route":4,
                                                "country":91,
                                                "sms":[
                                                        {
                                                            "message":sms,
                                                            "to":[adminNum]
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
                                    status = True
                                else:
                                    code = 4055
                                    Log.i('SMS notification could not be sent to admin to check the request')
                                    status = False
                            else:
                                code = 4040
                                message = "Invalid Appointment"
                                status = False
                                raise Exception
                            '''
                        elif self.apiId == 502022:
                            try:
                                docId = ObjectId(self.request.arguments.get('docId'))
                            except:
                                code = 4888
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
                            if serBook[0]['stage'] == 'accepted':
                                if serBook[0]['session_remaining'] <= 0:
                                    code = 4565
                                    status = False
                                    message = "Invalid Session Update"
                                    raise Exception
                                if serBook[0]['session_remaining'] == 1:
                                    serBookUpdate = self.doc_list.update_one(
                                                    {
                                                        '_id':docId
                                                    },
                                                    {
                                                    '$set':{
                                                            'stage':'completed'
                                                            },
                                                    '$inc':{
                                                            'session_remaining':-1
                                                            }
                                                    }
                                                )
                                    if serBookUpdate['n']:
                                        code = 2000
                                        status = True
                                        message = "Session is updated and booking is complete."
                                        sms = 'Greetings from Ohzas! Your session is complete\
                                                and your appointment for {} has been finished.\
                                            We look forward to provide service to you again. '.format(serName)
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
                                            message = "Request has been submitted and SMS notification has been sent"
                                            status = True
                                        else:
                                            code = 4055
                                            message = "Request has been submitted but the SMS notification could not be sent"
                                            status = False
                                    else:
                                        code = 4555
                                        status = False
                                        message = "Session could not be updated."
                                        raise Exception
                                else:
                                    erBookUpdate = self.doc_list.update_one(
                                                    {
                                                        '_id':docId
                                                    },
                                                    {
                                                    '$inc':{
                                                            'session_remaining':-1
                                                            }
                                                    }
                                                )
                                    if serBookUpdate['n']:
                                        code = 2000
                                        status = True
                                        message = "Session is updated."
                                    else:
                                        code = 4555
                                        status = False
                                        message = "Session could not be updated."
                                        raise Exception
                            else:
                                code = 2000
                                status = False
                                message = "Invalid Session Update"
                        else:
                            code = 4003
                            self.set_status(401)
                            message = 'You are not Authorized.'
                    else:
                        code = 4003
                        self.set_status(401)
                        message = 'You are not Authorized.'
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
                    Log.i(self.apiId)
                    if self.apiId in [ 502020, 502022]:
                        #TODO : Change ths code to 502022
                        if self.apiId == 502020:
                            Log.i('Clinic PUT req', self.request.arguments)

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
                                if stage == 'completed':
                                    sms = 'Greetings from Ohzas! Your appointment is complete. \
                                            We look forward to provide service to you again. '
                                elif stage == 'declined':
                                    sms = 'Greetings from Ohzas! We regret to inform you that your \
                                            appointment for {} has been cancelled. \
                                            We look forward to provide service to you again.'.format(serName)
                                elif stage == 'declined_fee':
                                    sms = 'Greetings from Ohzas! We regret to inform you that your \
                                            appointment for {} has been cancelled. \
                                            You will be charged \
                                            a cancellation fee in your next appointment.\
                                            We look forward to provide service to you again.'.format(serName)
                                    cancelUpdate = self.cancelFee.update_one(
                                                    {
                                                        'profileId':serBook[0]['profileId']
                                                    },
                                                    {
                                                    '$set':{
                                                                'profileId':serBook[0]['profileId'],
                                                                'cancellationFee':50,
                                                                'docId':docId,
                                                                'cancelTime':timeNow(),
                                                                'bookingTime':serBook[0]['booktime']
                                                            }
                                                    },
                                                    upsert=True
                                                )
                                else:
                                    sms = 'Hello! Greetings from Ohzas! Your appointement for {} has been {}'.format(serName,stage)
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
                                        message = "Request has been submitted and SMS notification has been sent"
                                        status = True
                                    else:
                                        code = 4055
                                        message = "Request has been submitted but the SMS notification could not be sent"
                                        status = False
                                else:
                                    code = 2000
                                    message = "Invalid booking"
                                    status = True
                            else:
                                code = 4070
                                status = False
                                message = "Invalid Option"

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

        #self.request.arguments =  json.loads(self.request.body.decode('utf-8'))
        try:
            areaId = int(self.request.arguments["aid"][0])
        except:
            areaId = None

        #Set the Doctor id if found in the request
        try:
            docId = str(self.request.arguments["did"][0].decode('utf-8'))
        except:
            docId = None

        #Set the Clinic id if found in the request
        try:
            clinicId = str(self.request.arguments["cid"][0].decode('utf-8'))
        except:
            clinicId = None

        try:
            # TODO: this need to be moved in a global class
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
                Log.i('ProfID', self.profileId)
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
                #Determine which app has sent it
                if len(app):
                    self.apiId = app[0]['apiId']
                    if app[0]['apiId'] in [ 502020, 502022]: # TODO: till here
                        #Handle the Clinic Doc list get request
                        #Show only the listed doctor for that clinic
                        if self.apiId == 502022:
                            Log.i('APIID', self.apiId)
                            if clinicId == None:
                                code = 4050
                                status = False
                                message = "Clinic ID Cannot be Empty"
                            else:
                                try:
                                    docId = ObjectId(docId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid doc Id"
                                resQ = self.clinic_list.find(
                                        {
                                            'clinicid':clinicId,
                                        }
                                    )
                                res = []
                                async for i in resQ:
                                    res.append(i)
                            #Res is from clinic_list collections whatevr matches
                            if len(res):
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
                            #Set the Area id if found in the request
                            Log.i('docId',docId)
                            Log.i('clinicId',clinicId)
                            #TODO : to check need of ObjectID check
                            if docId != None:
                                try:
                                    docId = ObjectId(docId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid docId Id"
                                    Log.i("Invalid Doc ID")

                            if clinicId != None:
                                try:
                                    clinicId = ObjectId(clinicId)
                                except:
                                    code = 4050
                                    status = False
                                    message = "Invalid Clinic Id"
                                    Log.i("Invalid Clinet ID")

                            #Doc and clinic both are None show all Docs in all clinics
                            if docId == None and clinicId ==None:

                                #resQ = self.doc_list.find()
                                resQ = await self.doc_list.count_documents({})
                                res = []
                                Log.i('Count of Docs ', resQ)
                                resQ = self.doc_list.find({})
                                async for i in resQ:
                                    i["_id"]=str(i["_id"])
                                    res.append(i)
                                Log.i('result ', res)

                                for doc in res:
                                    v= {"id": int(doc["docid"]), "doc": str(doc["docname"]) }
                                    result.append(v)

                            #Show thw list of all clinic  in that doc id
                            elif docId != None and clinicId == None:
                                resQ = self.doc_list.find(
                                        {
                                        }
                                    )
                                result = []
                                async for i in resQ:
                                    i["_id"]= str(i["_id"])
                                    i["clinicid"]= str(i["clinicid"])
                                    result.append(i)

                            #Show thw list of all doc  in that clinic id
                            elif docId == None and clinicId != None:
                                resQ = self.doc_list.find(
                                        {
                                            'clinicid':clinicId
                                        }
                                    )
                                result = []
                                async for i in resQ:
                                    i["_id"]= str(i["_id"])
                                    i["clinicid"]= str(i["clinicid"])
                                    result.append(i)
                            #Clinic and doc both provided Show the doc associated with the clinic
                            else:
                                Log.i("docid object",docId)
                                Log.i("clinicid object",clinicId)
                                resDoc = self.doc_list.find(
                                        {
                                            "_id": docId

                                        }
                                    )

                                result = []

                                async for i in resDoc:
                                    i["_id"]= str(i["_id"])
                                    i["clinicid"]= str(i["clinicid"])
                                    Log.i("Result",i)
                                    result.append(i)


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
