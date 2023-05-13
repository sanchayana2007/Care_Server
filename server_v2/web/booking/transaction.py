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
#User type configs 
admin_user = CONFIG['configs'][0]['admin_account']
clinic_user = CONFIG['configs'][0]['clinic_account']
patient_user = CONFIG['configs'][0]['user_account']
agent_user = CONFIG['configs'][0]['agent_account']


@xenSecureV1
class TransactionListHandler(tornado.web.RequestHandler):

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
    
    booking_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][4]['name']
                ]
    transaction_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][3]['name']
                ]
    slot_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][2]['name']
                ]

    paymentdata_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][6]['name']
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
                        # CONVERTS BODY INTO JSON
                        self.request.arguments = json.loads(self.request.body.decode())
                    except Exception as e:
                        code = 4100
                        message = 'Expected Request Type JSON.'
                        raise Exception
                    # TODO: this need to be moved in a global class, from here
                    try:
                        booking_id = str(self.request.arguments["booking_id"])
                       
                        
                    except:
                        code = 4888
                        message = "mandatory fields booking_id missing in request body "
                        raise Exception
                    
                    try:
                      
                        referenceid = str(self.request.arguments["referenceid"])
                      
                        
                    except:
                        code = 4888
                        message = "mandatory fields missing in request body referenceid "
                        raise Exception
                    

                    try:
                       
                        method = int(self.request.arguments["method"])
                        
                    except:
                        code = 4888
                        message = "mandatory fields method missing in request body "
                        raise Exception
                    

                    try:
                       
                        transactionstatus= str(self.request.arguments["transactionstatus"])
                        
                        
                    except:
                        code = 4888
                        message = "mandatory fields transactionstatus missing in request body "
                        raise Exception
                    try:
                     
                        transactionmethod = self.request.arguments["transactionmethod"]
                        
                    except:
                        code = 4888
                        message = "mandatory  transactionmethod fields missing in request body "
                        raise Exception
                    






                    self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)
                    #Determine which app has sent it
                    

                    if self.apiId:
                        Log.i(self.apiId)
                        #TODO : Change ths code to 502022
                        if self.apiId in [self.admin_user,self.clinic_user,self.agent_user,self.patient_user] and  method ==1 :
                            Log.i('Booking Post req', self.request.arguments)
                            result=[]
                            if booking_id != None  and transactionstatus != None :
                                #get the booing details from the booking table

                                booking  = await self.booking_list.find_one(
                                        {
                                           "_id":  ObjectId(booking_id),
                                           #"_id":  booking_id,
                                        },
                                        {
                                            "clinic_id": 1, 
                                            "doc_id" : 1, 
                                            "docname": 1,
                                            "clinicname": 1, 
                                             "slot_id": 1, 
                                             'seldate': 1, 
                                             'seldayhalf': 1,
                                             'netpatientpay': 1,
                                             'shopcommision': 1, 
                                             'accountid': 1, 
                                             'firstname': 1, 
                                             'lastname': 1, 
                                              'patientname': 1, 
                                             'phonenumber': 1, 
                                             'bookingstatus': 1,
                                              'token_no': 1, 

                                        }
                                        
                                    )

                                try:    
                                    
                                    if booking :
                                        print("Bookin data", booking)
                                        clinicid = booking["clinic_id"] 
                                        docid = booking["doc_id" ] 
                                        docname = booking["docname"]
                                        clinicname = booking["clinicname"] 
                                        slotId = booking["slot_id"] 
                                        seldate = booking['seldate'] 
                                        seldayhalf = booking['seldayhalf']
                                        netpatientpay= booking['netpatientpay']
                                        shopcommision = booking['shopcommision'] 
                                        accounid = booking['accountid'] 
                                        firstname = booking['firstname'] 
                                        lastname = booking['lastname'] 
                                        patient = booking['patientname'] 
                                        phoneNumber =      booking['phonenumber'] 
                                        bookingstatus =  booking['bookingstatus']
                                        tokenNo =  booking['token_no'] 
                                        print("Bookin data", booking)

                                    else:
                                        Log.i("No booking id found ")
                                        raise Exception    
                                except:
                                    code = 4888
                                    message = "No booking id found"
                                    raise Exception
                                

                                #Handle When the transcation is failed 
                                if transactionstatus== "SUCCESS":
                                    Bookingstatusfinal = "SUCCESS"
                                    Log.i("Transaction has gone succesfully ")
                                    if bookingstatus == "PENDING":
                                        #Update the booking status as SUCCESS
                                        updatebooking  = await self.booking_list.update_one(
                                            {
                                                "_id":  ObjectId(booking_id),
                                            },
                                            {
                                                '$set':{
                                                            'bookingstatus':'SUCCESS'
                                                    },
                                            }


                                        )
                                    elif bookingstatus == "SUCCESS":
                                        Bookingstatusfinal = "SUCCESS"
                                        #Update the booking status as SUCCESS
                                        updatebooking  = await self.booking_list.update_one(
                                            
                                            {
                                                "_id":  ObjectId(booking_id),
                                            },
                                            {
                                            '$set':{
                                                            'bookingstatus':'DOUBLESUCCESS'
                                            },
                                            }
                                        )
                                    else:
                                        print("Unknown Booking status")
                                        pass

                                else:
                                    Log.i("Transaction has FAILED ")        
                                    if bookingstatus == "PENDING":
                                        #Update the booking status as SUCCESS
                                        Bookingstatusfinal = "FAILED"
                                        updatebooking  = await self.booking_list.update_one(
                                            {
                                                "_id":  ObjectId(booking_id),
                                            },
                                             {  
                                                
                                                '$set':{
                                                            'bookingstatus':'FAILED'
                                            }
                                             }

                                        )

                                                                            
                                        resSlot = await self.slot_list.update_one(
                                                {
                                                     "_id":  ObjectId(slotId),
                                                },
                                                {
                                                '$inc':{
                                                           # 'monthly_slots.'+ seldate +"."+ avslots : -1
                                                            'monthly_slots.'+ seldate +"."+ seldayhalf : 1
                                                       }
                                                }
                                            )
                                       
                                        #Update the slotlist by decrementing the slot 
                                        Update_Succesfull = resSlot.modified_count

                                        Log.i("resSlot", Update_Succesfull) 

                                        
                                    elif bookingstatus == "SUCCESS":
                                        #Update the booking status as SUCCESS
                                        Bookingstatusfinal = "PARTIALSUCCESS"
                                        updatebooking  = await self.booking_list.update_one(
                                            {
                                                "_id":  ObjectId(booking_id),
                                            },
                                            {
                                                    'bookingstatus': "CONFLICT",
                                            }

                                        )
                                    else:
                                        print("Unknown Booking status")
                                        pass


                                slotno =  'monthly_slots.'+ seldate

                                restransaction = await self.transaction_list.insert_one(
                                            {
                                                     
                                                    "clinic_id":  clinicid,
                                                    "doc_id" : docid,
                                                    "docname": docname,
                                                    "clinicname": clinicname,
                                                    
                                                    'seldate': seldate,
                                                    'seldayhalf':seldayhalf,
                                                    'netpatientpay':netpatientpay,
                                                    'shopcommision': shopcommision,
                                                    'accountid': accounid,
                                                    'firstname': firstname,
                                                    'lastname': lastname, 
                                                    'patientname': patient,
                                                    'phonenumber': phoneNumber,
                                                    'bookingstatus' : "PENDING",
                                                    'token_no': tokenNo,
                                                    'bookingid':  ObjectId(booking_id),
                                                    
                                                    'timeofbooking': timeNow()

                                                    }
                                                )
                                transaction_id = str(restransaction.inserted_id)
                                print(transaction_id)
                                if transaction_id :
                                    Log.i("transaction Id created ")
                                    code = 2000
                                    message = "transaction ID created "
                                    result = []
                                    result.append({"transactionid": transaction_id,"bookingfinalstatus":Bookingstatusfinal,
                                    "ConfirmedToken": tokenNo , "Timming": "YTD"
    
                                    })
                                    status = True
                                else:
                                    Log.i("transaction Id not created ")
                                    code = 4000
                                    message = "transaction ID not  created "
                                    status = True
                                    


                                '''    
                                #Res is from clinic_list collections whatevr matches
                                if slots:

                                    slots_available=slots['monthly_slots'][seldate][str(seldayhalf)]
                                    #totalslots=slots['monthly_slots'][seldate][str(seldayhalf)]
                                    totalslots=20
                                    netpatientpay=slots['netpatientpay']
                                    shopcommision=slots['shopcommision']
                                    emergency=slots['emergency']

                                    refundoncancelpay=slots['refundoncancelpay']

                                    #we found a slot and try booking
                                    if slots_available > 0:
                                        Log.i('slots_available ',slots_available)
                                        resSlot = await self.slot_list.update_one(
                                                {
                                                    "clinic_id":  clinicId,
                                                    "doc_id" : docId
                                                    #'monthly_slots.'+ seldate + seldayhalf : {'$gt': 0}
                                                },
                                                {
                                                '$inc':{
                                                            'monthly_slots.'+ seldate +"."+ seldayhalf : 20
                                                       }
                                                }
                                            )
                                        Log.i("resSlot", resSlot.modified_count)
                                        Log.i("apiID",self.apiId)
                                        booking_id = random.randint(0, 5)
                                        if resSlot.modified_count ==1:
                                            resbooking = await self.booking_list.insert_one(
                                                    {
                                                        "_id": booking_id,
                                                        "entitiId" : self.entityId,
                                                        "accountId": self.accountId,
                                                        "applicationId": self.applicationId,
                                                        "apiid": self.apiId,
                                                        "clinic_id":  clinicId,
                                                        "doc_id" : docId,
                                                        "slot_no": slots_available,
                                                        'seldate': seldate,
                                                        'seldayhalf':seldayhalf,
                                                        'netpatientpay':netpatientpay,
                                                        'shopcommision': shopcommision,
                                                        'emergency': emergency,
                                                        'refundoncancelpay' : refundoncancelpay,
                                                        'slotstatus' : "PENDING",
                                                        'totalslots': totalslots,
                                                        'token_no':None,
                                                        'ampm':seldayhalf,
                                                        'inserttime': timeNow()

                                                    }
                                                )
                                            Log.i("resSlot", resSlot.modified_count)
                                            booking_dict={}
                                            booking_dict['bookingid']=booking_id
                                            if self.apiId == 502020:
                                                booking_dict['Amountpay']=netpatientpay
                                            else:
                                                booking_dict['Amountpay']=netpatientpay + shopcommision
                                            result.append(booking_dict)

                                    else:
                                        Log.i('slots_Unavialiable',slots_available)


                                    code = 2000
                                    status = True
                                    message = "Doctors Found in Clinic"
                                    
                                else:
                                    code = 4080
                                    status = False
                                    message = "No Slot data found"
                                '''

                                #Log.i("datestr",type(resDoc))
                                #Log.i("datestr", resDoc.modified_count)

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
                        elif self.apiId in [self.admin_user,self.clinic_user,self.agent_user,self.patient_user]:
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

                if self.apiId in [self.admin_user,self.clinic_user,self.agent_user,self.patient_user]: # TODO: till here
                    #Handle the Clinic Doc list get request
                    #Show only the listed doctor for that clinic
                    if self.apiId in [self.admin_user,self.clinic_user]:
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
                    elif self.apiId in [self.admin_user,self.agent_user,self.patient_user]:
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