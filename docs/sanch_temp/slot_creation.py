from datetime import date,datetime,timedelta
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



def create_slots_type1(Filling_days,weekdaysno,ampmvists,SlotsAM,SlotsPM,visibility):
    slots={}
    weekdaysname=["MON","TUE","WED","THU","FRI","SAT","SUN"]
    #create Current Date and determine 
    today= date.today()
    print("test1",weekdaysno)
    ampmvists= Convert(ampmvists)
    SlotsAM= Convert_2(SlotsAM)
    SlotsPM= Convert_2(SlotsPM)
   
    for i in  range(0,Filling_days,1):
        avdayslots={}
        nvdayslots={}
        avdayslots['visibility'] = visibility
        nvdayslots['visibility'] = visibility
        
        #determine teh current date
        date_time = today.strftime("%d/%m/%Y")
        print("date_time", date_time)
        
        weekday = datetime.weekday(today)
        weekdaysno= Convert(weekdaysno)
        #print("test2 ampmvists SlotsAM SlotsPM weekdaysno",ampmvists, SlotsAM, SlotsPM, weekdaysno)
        #date_time = datetime.strftime("%d/%m/%Y")
        print("Weekday",weekdaysname[weekday], "weekdaysno",weekdaysno,"date and time:",date_time)
        if str(weekday) in  weekdaysno:
            ind= weekdaysno.index(str(weekday))
            #print('ind',ind)
            if ampmvists[ind]=='b':
                avdayslots['tAM']=int(SlotsAM[ind])
                avdayslots['aAM']=int(SlotsAM[ind])
                avdayslots['tPM']=int(SlotsPM[ind])
                avdayslots['tPM']=int(SlotsAM[ind])

            elif ampmvists[ind]=='a':
                avdayslots['tAM']=int(SlotsAM[ind])
                avdayslots['aAM']=int(SlotsAM[ind])
                avdayslots['tPM']=0
                avdayslots['aPM']=0
            elif ampmvists[ind]=='p':
                avdayslots['tPM']=int(SlotsPM[ind])
                avdayslots['aPM']=int(SlotsPM[ind])
                avdayslots['tAM']=0
                avdayslots['aAM']=0
            else:
                pass
            avdayslots['daytext']=""
            avdayslots['dayofweek']=weekdaysname[weekday]
            slots[date_time]= avdayslots

        #    print("FOUND Weekday",weekday, "weekdaysno",weekdaysno,"date and time:",date_time)
        else:
            nvdayslots['tAM']= 0 
            nvdayslots['aAM']= 0
            nvdayslots['tPM']= 0
            nvdayslots['tPM']= 0
            nvdayslots['daytext']=""
            nvdayslots['dayofweek']=weekdaysname[weekday]
            slots[date_time]= nvdayslots

        today = today +  timedelta(days=+1)
        print("today at last", today)
    #print("Slots",slots)
    return slots

print(create_slots_type1(10,"123","bpa","030405","030405",True))
