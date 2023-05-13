import time
from datetime import date,datetime,timedelta
def create_slots_doc(slottotaldays,slotData):
    slots={}
    today= date.today()
    print("test1",slotData)
   
   
    for i in  range(0,slottotaldays,1):
        avdayslots={}
        nvdayslots={}
        avdayslots['visibility'] = False
        nvdayslots['visibility'] = False
            
       
        
        weekday = datetime.weekday(today)
        #date_time = datetime.strftime("%d/%m/%Y")
        date_time = today.strftime("%d/%m/%Y")
        print("Weekday",weekday, "date and time:",date_time, slotData[weekday])
        
        if slotData[weekday]:
            slots[date_time]= slotData[weekday]
        else:
            print(str(slotData[weekday])+ "Is not a valid weekday")
           
        today = today +  timedelta(days=+1)


    #print("Slots",slots)
    return slots

s= [{'morning': {'startTime': '01:01 PM', 'endTime': '04:21 PM'}, 'evening': {'startTime': '07:00 PM', 'endTime': '09:00 PM'}, 'nOp': 6, 'day': 'Monday'}, {'morning': {'startTime': '01:01 PM', 'endTime': '04:21 PM'}, 'evening': {'startTime': '07:00 PM', 'endTime': '09:00 PM'}, 'nOp': 6, 'day': 'Tuesday'}, {'morning': {'startTime': '01:01 PM', 'endTime': '04:21 PM'}, 'evening': {'startTime': '07:00 PM', 'endTime': '09:00 PM'}, 'nOp': 6, 'day': 'Wednesday'}, {'morning': {'startTime': '01:01 PM', 'endTime': '04:21 PM'}, 'evening': {'startTime': '07:00 PM', 'endTime': '09:00 PM'}, 'nOp': 6, 'day': 'Thursday'}, {'morning': {'startTime': '01:01 PM', 'endTime': '04:21 PM'}, 'evening': {'startTime': '07:00 PM', 'endTime': '09:00 PM'}, 'nOp': 6, 'day': 'Friday'}, {'morning': {'startTime': '01:01 PM', 'endTime': '04:21 PM'}, 'evening': {'startTime': '07:00 PM', 'endTime': '09:00 PM'}, 'nOp': 6, 'day': 'Saturday'}, {'morning': {'startTime': '01:01 PM', 'endTime': '04:21 PM'}, 'evening': {'startTime': '07:00 PM', 'endTime': '09:00 PM'}, 'nOp': 6, 'day': 'Sunday'}]
create_slots_doc(10, s)


