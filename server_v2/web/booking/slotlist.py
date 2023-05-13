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
class SlotListHandler(tornado.web.RequestHandler):

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
    doc_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][0]['name']
                ]
    clinic_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][1]['name']
                ]
    slot_list  = MongoMixin.medicineDb[
                    CONFIG['database'][2]['table'][2]['name']
                ]
    #User type configs 
    admin_user = CONFIG['configs'][0]['admin_account']
    clinic_user = CONFIG['configs'][0]['clinic_account']
    patient_user = CONFIG['configs'][0]['user_account']
    agent_user = CONFIG['configs'][0]['agent_account']


    fu = FileUtil()
    #Post is admin run for 30 days pre polpulate slots
    async def post(self):
        print("Slot Add ")

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
           
            try:
               
                # CHECK method field si set 
                method = int(self.request.arguments["method"])
            except Exception as e:
                code = 4100
                message = 'method is not set '
                raise Exception

            #Determine which app has sent it
            self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)  
                 
            if self.apiId:    
                # Doc and Slot created by admin or clinic user for the first time 
                if self.apiId in [self.admin_user,self.clinic_user,self.agent_user,self.patient_user] and method == 1:
                    docdetails = []
                    slotdetails=[]
                    monthly_slots = {}
                    #The slodata is Total number of days to filled 
                    #This value should be taken form teh application column 
                    slottotaldays = 180
                    

                    try:
                        print("Slot Add 1") 
                        #Mandatory the field Validation needs to be checked by APP
                        slotDate  = datetime.date.today()
                                              
                        #All records from
                        docID = None
                        clinicId = None #App populated
                        clinicId = self.request.arguments.get("clinicid")
                        
                        #Doc details 
                        docspeciality = self.request.arguments.get("docspeciality")
                        docname = self.request.arguments.get("docname")
                        countryCode = self.request.arguments.get("countryCode")
                        docfees = self.request.arguments.get("docfees")
                        docphone = self.request.arguments.get("docphone")
                        slotdata = self.request.arguments.get("slotdata")
                        docomment = self.request.arguments.get("docomment")
                        expirence = self.request.arguments.get("expirence")
                        Log.i('slotDate', slotDate)
                        Log.i('Slot',type(slotdata))

                    except:
                        code = 4888
                        message = "Invalid Request Body "
                        raise Exception
                    #Get all the records from the doctor list
                    print("Slot Add 1")
                    #Get the Clinic Id is  found n teh clinic info table 
                    clinicQ = self.clinic_list.find(
                    {
                       '_id': ObjectId(clinicId)
                    },
                    {
                        'clinic_name':1,
                        'cliniclocation': 1,
                        'clinicaddress': 1,
                        'pocclinicph': 1,
                        'paymentadd': 1,
                        'clinicpaymentaddress': 1,
                        'pin':1,
                        'comment':"Entry test "
                    },
                    limit=1
                    )
                    clinicdetails=[]

                    #Clinic id is found                             
                    async for i in clinicQ:
                        clinicdetails.append(i)
                        Log.i("clinicdetails",clinicdetails)
                            
                    if len(clinicdetails):
                                                   
                        monthly_slots['monthly_slots']= create_slots_doc(slottotaldays,slotdata)
                        monthly_slots['docname']= docname
                        monthly_slots['docomment']= docomment
                        monthly_slots['clinicname']= clinicdetails[0]['clinic_name']
                        #monthly_slots['docid']= docId
                        monthly_slots['clinicid']= clinicdetails[0]['_id']
                        monthly_slots['default_monthly_slot'] = slotdata
                        cliniclocation = clinicdetails[0]['cliniclocation']
                        pin = clinicdetails[0]['pin']
                        #Log.i("monthly_slots",monthly_slots)

                        #Insert in doc details 
                        av_list = Av_weekdays(slotdata)
                        print("AV_LIST",av_list)

                        docId = self.doc_list.insert_one(
                            {
                                'docname': docname,
                                'clinicname' : clinicdetails[0]['clinic_name'],
                                'clinicid': clinicdetails[0]['_id'], 
                                'speciality': docspeciality ,
                                'weekly_availability': av_list,
                                'cliniclocation': cliniclocation,
                                'clinicid': clinicId,
                                'pin': pin,
                                'docfees': docfees,
                                'expirence': expirence,
                                'docphone': docphone
                            }
                        )
                        if docId:
                            docId = await docId

                            Log.i("docid inserted",docId.inserted_id )
                            monthly_slots['docid']= docId.inserted_id
                            #This is payment code we will use later 
                            #Default payment code can be changed accordingly 
                            monthly_slots['paymentid']= 100
                            
                            SlotId = self.slot_list.insert_one(monthly_slots.copy())
                            if SlotId:
                                result = []
                                SlotId = await SlotId
                                SlotId = str(SlotId.inserted_id)
                                Log.i("SlotId inserted", SlotId )

                                code = 2000
                                message = "SlotId is has been added"
                                result.append({"Slotid": SlotId})
                                status = True
                            else:
                                Log.i("SlotId not inserted")
                                code = 5010
                                message = "Error in SlotId addition"
                                status = True


                    else:
                        message = "NoClinic id is found with doc details "
                        raise Exception
                        


                #All GET METHODS 
                # Handling the get for showing all slots to everyone 
                # This is with clinic and docid we can change this input to slot id only 
                elif self.apiId in [self.admin_user,self.clinic_user,self.agent_user,self.patient_user] and method == 2:
                    Log.i("getting the slot details ")
                    
                    try:
                        clinicId = self.request.arguments.get("clinicid")
                        docId = self.request.arguments.get("docid")
                    except:
                        code = 4888
                        message = "mandatory field doc or clinic  id is missing  "
                        raise Exception

                    #Doc details 
                    #print( slotId)
                    slotQ = self.slot_list.find(
                    {
                        "clinicid":  ObjectId(clinicId),
                        "docid": ObjectId(docId)


                    },
                    {
                       'monthly_slots':1
                    },
                    limit=1
                    )
                    slotdetails=[]
                    if slotQ:
                        #Clinic id is found 
                        result = []                         
                        async for i in slotQ:
                            slotdetails.append(i)
                            i["_id"]= str(i["_id"])
                            result.append(i)
                        
                        if len(result):
                            result1 = {}
                            Slotdatalisted = create_slots_list(result[0]['monthly_slots'],10)
                            print(Slotdatalisted)
                            result1["Slotdata"] = Slotdatalisted
                            result1["Slotid"] = result[0]['_id']
                            result = result1
                            code = 2000
                            status = True
                            Log.i("slotdetails",result)
                            message = "Slot details found "
                        else:
                            code = 4080
                            status = False
                            message = "No Slot data found for ClinicId and docid"
                    
                    else:
                        code = 4080
                        status = False
                        message = "No SlotQ found"
                
                # Handling scenerios for view/modification of default slots 
                # 
                elif self.apiId in [self.admin_user,self.clinic_user] and method == 3:
                    #Log.i("getting/Showing the  default Slot data ")
                    try:
                        clinicId = self.request.arguments["clinicid"]
                        docId = self.request.arguments["docid"]
  
                    except:
                        code = 4888
                        message = "mandatory field Slot id is missing  "
                        raise Exception



                    #Doc details 
                    slots  = await self.slot_list.find_one(
                                        {
                                           "clinicid":  ObjectId(clinicId),
                                            "docid": ObjectId(docId)
                                            

                                        },
                                        {
                                            'docname': 1,
                                            'clinicname':1,
                                            'clinicid':1,
                                            'docid':1,
                                            'docomment':1,
                                            'default_monthly_slot'  :1 
                                        }
                                        
                                    )

                    
                    
                    if slots:
                        #Slot id is found 
                        doctor  = await self.doc_list.find_one(
                                        {
                                            "_id":  slots['docid'],
                                            

                                        },
                                        {
                                            'docname': 1,
                                            'clinicname':1,
                                            'docfees':1,
                                            'docphone':1
                                             
                                        }
                                        
                                    )
                        if doctor:
                            

                            result =  [{'docfees': doctor['docfees'],'docphone': doctor['docphone'],'docname': slots['docname'], 'default_monthly_slots': slots['default_monthly_slot'],'clinicname': slots['clinicname'] ,'doccomment': slots['docomment']}]                         
                            code = 2000
                            status = True
                            message = "Slots found"
                        
                        else:
                            #result =  [{'docfees': doctor['docfees'],'docphone': doctor['docphone'],'docname': slots['docname'], 'default_monthly_slots': slots['default_monthly_slot'],'clinicname': slots['clinicname'] ,'doccomment': slots['docomment']}]                         
                            code = 4000
                            status = True
                            message = "No Doctor  found with associated with this slot"
                        
                    
                    else:
                        code = 4080
                        status = False
                        message = "No SlotQ found"
                # Get the slot for a Single date 
                elif self.apiId in [self.admin_user,self.clinic_user,self.patient_user] and method == 4:
                    #Log.i("getting/Showing the  default Slot data ")
                    try:
                        slotId = self.request.arguments.get("slotid")
                        datequery = self.request.arguments.get("date")
                    except:
                        code = 4888
                        message = "mandatory field Slot id  or Date is missing  "
                        raise Exception

                    if slotId != None  and datequery != None :
                        Log.i(datequery)
                        slotno =  'monthly_slots.'+ datequery

                        # Lets Validate  the slot and if its found 
                        slots  = await self.slot_list.find_one(
                                {
                                    "_id":  ObjectId(slotId),
                                
                                },
                                {
                                    'docname': 1,
                                    'clinicname':1,
                                    'paymentid':1, 
                                    'clinicid':1,
                                    'docid':1,
                                    slotno :1 
                                }
                                
                                    )

                        print("Slots",slots)
                    
                        if slots:
                            #Slot id is found 
                            doctor  = await self.doc_list.find_one(
                                            {
                                                "_id":  slots['docid'],
                                                
    
                                            },
                                            {
                                                'docname': 1,
                                                'clinicname':1,
                                                'docfees':1,
                                                'docphone':1
                                                 
                                            }
                                            
                                        )
                        if doctor:
                            

                            result =  [{'docfees': doctor['docfees'],'docphone': doctor['docphone'],'docname': slots['docname'], 'day_slots': slotno,'clinicname': slots['clinicname'] ,'doccomment': slots['docomment']}]                         
                            code = 2000
                            status = True
                            message = "Slots found"
                        
                        else:
                            #result =  [{'docfees': doctor['docfees'],'docphone': doctor['docphone'],'docname': slots['docname'], 'default_monthly_slots': slots['default_monthly_slot'],'clinicname': slots['clinicname'] ,'doccomment': slots['docomment']}]                         
                            code = 4000
                            status = True
                            message = "No Doctor  found with associated with this slot"
                        
                    
                    else:
                        code = 4080
                        status = False
                        message = "No SlotQ found"

                      
                    
                else:

                    

                     pass 

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
            

            # TO
            
            self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)
                #Determine which app has sent it
           
            method = self.request.arguments["method"] 
            print("PUT",self.apiId , self.admin_user,self.clinic_user,method )
                #Edit a day slot 

                #Edit defalt data and populate the Slots 
            if self.apiId  in [self.admin_user,self.clinic_user] and method ==1:
                Log.i('Slot PUT req', self.request.arguments)
                try :
         
                    clinicId = self.request.arguments["clinicid"]
                    docId = self.request.arguments["docid"]
                    
                except:
                    code = 4800
                    message = 'Mandatory parameter Missing.'
                    raise Exception
                        
                result=[]
                if clinicId  != None and docId  != None:
                    #Doc details 
                    docspeciality = self.request.arguments.get("docspeciality")
                    docname = self.request.arguments.get("docname")
                    countryCode = self.request.arguments.get("countryCode")
                    docfees = self.request.arguments.get("docfees")
                    docphone = self.request.arguments.get("docphone")
                    slotdata = self.request.arguments.get("slotdata")
                    docomment = self.request.arguments.get("docomment")
                        
                    #Doc details 
                    slottotaldays =90
                    slotdatesupdated = create_slots_doc(slottotaldays,slotdata)
                    Log.i('Slot slotdatesupdated ')
                    slot_update = await self.slot_list.find_one_and_update(
                                       {
                                           "clinicid":  ObjectId(clinicId),
                                            "docid": ObjectId(docId)
                                            

                                        },
                                        {
                                            '$set':   {
                                                'docname': docname,
                                                'docomment': docomment,
                                                'default_monthly_slot': slotdata,
                                                'monthly_slots': slotdatesupdated
                                            }
                                        }
                                        
                                    )

                    
                    #Slot Update 
                    if slot_update:
                        Log.i('Slot slot_update ',slot_update)
                        #Get the doc id 
                        doctorQ  = await self.slot_list.find_one(
                                    {
                                       "clinicid":  ObjectId(clinicId),
                                        "docid": ObjectId(docId)
                                        
                                    },
                                    {
                                        'docid': 1
                                                                                 
                                    }
                                    
                                    )
                        if doctorQ:
                            Log.i('Slot slot_update ',doctorQ )
                            #We have got a doctor update the doctor data 
                            doc_update = await self.doc_list.find_one_and_update(
                                            {
                                                "_id":  ObjectId(doctorQ['docid']),


                                            },
                                            {
                                                '$set':   {
                                                    'docname': docname,

                                                    'speciality': docspeciality ,

                                                    'docfees': docfees,
                                                    'docphone': docphone
                                                }
                                            }

                                        )

                            print("doc_update",doc_update)
                            Update_Succesfull = str(doc_update['_id'])
                            if Update_Succesfull :
                                result =  [{ 'doc_id': Update_Succesfull}]                         
                                code = 2000
                                status = True
                                message = "Slots Updated Succesfully"
                        
                            else:
                                result =  [{}]                         
                                code = 4000
                                status = True
                                message = "Slots NotUpdated "
                        
                        else:
                           
                            status = True
                            message = "No Doctor  found with associated with this slot"
            #Open 
            elif  self.apiId  in [self.admin_user,self.clinic_user] and method ==2:
                    updatecount=0 
                    try :
                
                        datelist = self.request.arguments["datelist"]
                    
                    except:
                        code = 4800
                        message = 'Mandatory parameter Missing.'
                        raise Exception


                    try:
                        clinicId = self.request.arguments.get("clinicid")
                        docId = self.request.arguments.get("docid")
                    except:
                        code = 4888
                        message = "mandatory field doc or clinic  id is missing  "
                        raise Exception
                    
                    for seldate in datelist:    
                        print(seldate)
                        #convert the date in the DD/MM/YYYY
                        dated_list = seldate.split(' ')[0].split('-')
                        seldate= dated_list[2] + '/' + dated_list[1] + '/' + dated_list[0] 
                        print("Seldate",seldate)
                        updatecount +=1

                       
                        resSlot = await self.slot_list.find_one_and_update(
                                        {
                                            "clinicid":  ObjectId(clinicId),
                                            "docid": ObjectId(docId),
                                            #"clinicid":  clinicId,
                                            #"docid": docId,
                                            #'monthly_slots.'+ seldate +".Visibility" : False
                                        },
                                        {
                                        '$set':{
                                                  
                                                'monthly_slots.'+ seldate +".Visibility" : True
                                               }
                                        }
                                    )
                        print("Slot_visbility_update",resSlot, updatecount)
                        
                        if resSlot:
                            Update_Succesfull = str(resSlot['_id'])
                            if Update_Succesfull :
                                result =  [{'upadtedid': Update_Succesfull}]                         
                                code = 2000
                                status = True
                                message = "Slots Updated Succesfully"

                            else:
                                result =  [{}]                         
                                code = 4000
                                status = True
                                message = "Slots NotUpdated "
                                #Typical SMS gateway integration
                  
                #Editing a single day    
            elif self.apiId  in [self.admin_user,self.clinic_user] and method ==3:
                    #updatecount=0 
                    pass
                
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
        
        try :
            self.request.arguments =  json.loads(self.request.body)
        except Exception as e:
            print(e)
            raise Exception
            

        areaId = self.request.arguments["aid"]
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

                            print("docId clinicId seldate",docId,clinicId, seldate)
                            resDoc = self.slot_list.find(
                                    {
                                        "clinic_id":  clinicId,
                                        "doc_id" : docId
                                    }

                                )
                            print("resDoc",resDoc)
                            
                            async for i in resDoc:
                                i["_id"]= str(i["_id"])
                                #datedata= i["monthly_slots"][seldate]
                                #result.append(datedata)
                                result.append(i)
                            Log.i("datestr",result)

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
                self.request.arguments = json.loads(self.request.body.decode())
            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception
            try:
                # CONVERTS BODY INTO JSON
                method = self.request.arguments["method"]
                clinicId = self.request.arguments["clinicid"]
                docId = self.request.arguments["docid"]
                

            except Exception as e:
                code = 4100
                message = 'Expected Request Type JSON.'
                raise Exception

            #Determine which app has sent it
            self.apiId  = await validate_profile(self.entityId,self.accountId,self.applicationId)            
            if self.apiId:    
                # Doc and Slot created by admin or clinic user for the first time 
                if self.apiId in [self.admin_user,self.clinic_user] and method == 1:
                    slotId = self.request.arguments.get("slotid")
                    slotQ = self.slot_list.find(
                    {
                       "clinicid":  ObjectId(clinicId),
                        "docid": ObjectId(docId)

                    },
                    {
                        'docid':1,
                      
                    },
                    limit=1
                    )
                    slotdetails=[]

                    #Clinic id is found                             
                    async for i in slotQ:
                        slotdetails.append(i)
                        Log.i("slotdetails",slotdetails)
                    #Doc details 
                    if  len(slotdetails):
                        docId= slotdetails[0]['docid']

                        delslot = self.slot_list.delete_one({ "clinicid":  ObjectId(clinicId),
                        "docid": ObjectId(docId)})
                        deldoc = self.doc_list.delete_one({'_id': docId })
                        code= 2000
                        status = False
                        message = "Slot and Doc is deleted"

                       
                    else:
                        code= 4055
                        status = False
                        message = "Doc not found  Not  Found"


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
