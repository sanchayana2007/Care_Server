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
from ..lib.lib import *
import requests
import http.client
import datetime




@xenSecureV1
class CancellationListHandler(tornado.web.RequestHandler):

    SUPPORTED_METHODS = ('POST','PUT','DELETE')

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
    transaction_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][3]['name']
                ]
    booking_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][4]['name']
                ]
    slot_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][2]['name']
                ]
    cancellation_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][7]['name']
                ]

     #User type configs 
    admin_user = CONFIG['configs'][0]['admin_account']
    clinic_user = CONFIG['configs'][0]['clinic_account']
    patient_user = CONFIG['configs'][0]['user_account']
    agent_user = CONFIG['configs'][0]['agent_account']


    fu = FileUtil()
    
    #Post is admin run for 30 days pre polpulate slots
    async def post(self):
                status = False
                code = 4000
                result = []
                message = ''

                try:
                    try:
                        # CONVERTS BODY INTO
                              
                        self.request.arguments = json.loads(self.request.body.decode())
                    except Exception as e:
                        code = 4100
                        message = 'Expected Request Type JSON.'
                        raise Exception
                    # TODO: this need to be moved in a global class, from here
                    try:
                        
                        method = self.request.arguments["method"]
                    
                    except:
                        code = 4888
                        message = "mandatory fields missing in request body "
                        raise Exception
                    
                    
                    self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)
                    #Determine which app has sent it
                    
                    
                    #Log.i("UserAcc",accountQ['firstName'])
                  

                    if self.apiId:
                        Log.i(self.apiId)
                        #TODO : Change ths code to 502022
                        #Cancellation for user patient_user
                        if self.apiId in [self.admin_user,self.patient_user] and method == 1:
                            transId = str(self.request.arguments["transactionid"])
                            Log.i('Cancellation for user req', self.request.arguments)
                            result=[]
                            if transId != None  :
                               

                                # Lets Validate  the slot and if its found 
                                transaction  = await self.transaction_list.find_one(
                                        {
                                            "_id":  ObjectId(transId),
                                            

                                        },
                                        {
                                            'docname': 1,
                                            'clinicname':1,
                                            'paymentid':1, 
                                            'clinicid':1,
                                            'netpatientpay': 1, 
                                            'shopcommision' :1 ,
                                            'bookingstatus': 1
                                            
                                        }
                                        
                                    )

                                print("transaction",transaction)
                                    
                                bookingstatus= transaction["bookingstatus"]
                                if bookingstatus == "SUCCCESS":
                                    #we are fit for cancellation 
                                                                  
                                    #Update the slotlist by decrementing the slot 
                                    Update_Succesfull = resSlot.modified_count

                                    Log.i("resSlot", Update_Succesfull) 
                                    #Update teh booking record  
                                    if Update_Succesfull == 1:
                                        rescancel = await self.cancellation_list.insert_one(
                                                    {
                                                     
                                                        "clinic_id":  clinicid,
                                                        "doc_id" : docid,
                                                        "docname": docname,
                                                        "clinicname": clinicname,
                                                        "tarnsaction_id": transId,
                                                        'seldate': datetime.date(),
                                                        'status': 'REFUND_INIT', 
                                                        'slotid': 'NEED TO BE UPDATED from transaction',
                                                        'phonenumber': phoneNumber,
                                                                                                               
                                                        'timeofbooking': timeNow()

                                                    }
                                                )
                                            
                                        if rescancel:

                                            result = []
                                            Log.i("cancellationid  Id created ")
                                            code = 2000
                                            message = "Cancellation is accepted "
                                            result.append({"booking_id": booking_id,"netpatientpay":netpatientpay,
                                                "docname":docname,"clinicname":clinicname , "status": "PENDING"
                                            })
                                            status = True


                            #Cancellation is for a day done by clinic                 
                            elif  self.apiId in [self.admin_user,self.clinic_user] and method == 2:
                                slotId = str(self.request.arguments["slot_id"])
                                
                                seldate= str(self.request.arguments["date"])
                                #set the visbility in slot[slotlist] as False and doccommment 

                                #get all the user succesfully booked[bookinglist] for the slot for that day 
                                #bookingstatus== CANCEL 
                                


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
            bookingId = int(self.request.arguments["bookingid"])
            price = str(self.request.arguments["price"])
            transactionRef = str(self.request.arguments["transactionref"])
            transactionRef2 = str(self.request.arguments["transactionref2"])
            patientId = str(self.request.arguments["cid"])
            method = str(self.request.arguments["method"])
            Status = str(self.request.arguments["status"])
            application = str(self.request.arguments["application"])
            os = str(self.request.arguments["os"])
            clientIP = str(self.request.arguments["clientip"])
            Log.i("areaId",areaId)
            Log.i("bookingId",docId)
            Log.i("clinicId",clinicId)

            self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)
            #Determine which app has sent it
            if self.apiId:
                Log.i(self.apiId)
                #TODO : Change ths code to 502022
                if self.apiId == 502020:
                    Log.i('Booking PUT req', self.request.arguments)
                    result=[]
                    if docId != None and clinicId != None and seldate != None:

                        Log.i(seldate)
                        booking_list  = await self.booking_list.find_one(
                                {
                                    "_id":  bookingid,

                                },
                                {
                                    slots_no:1,
                                    totalslots:1

                                }
                            )
                        tokenno=booking_list['totalslots'] -  booking_list['slots_no']
                        #Res is from clinic_list collections whatevr matches
                        if Status == 1:
                            slotstatus = "CONFIRMED"
                        else:
                            slotstatus = "REJECTED"

                            booking_list  = await self.booking_list.update_one(
                                    {
                                        "_id":  bookingid,
                                    },
                                    {
                                    '$set':{
                                                'slotstatus': slotstatus,
                                                'transactionstatus': Status,
                                                'token': tokenno
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
