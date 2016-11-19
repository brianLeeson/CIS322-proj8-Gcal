from process_events import *

def test_relevantEvents():
  
  #Test 1 - normal. 1 event provided, 1 event created
  eventList = [{'organizer': {'email': 'cyberjunkie09@gmail.com', 'self': True, 'displayName': 'Brian Leeson'}, 'kind': 'calendar#event', 'id': '64o6cob56tj62b9hckqm8b9k71h62b9o6oq3cb9n6so62o9j61hj6ohp6g', 'start': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-11-16T06:00:00-08:00'}, 'updated': '2016-11-15T21:42:03.235Z', 'htmlLink': 'https://www.google.com/calendar/event?eid=NjRvNmNvYjU2dGo2MmI5aGNrcW04YjlrNzFoNjJiOW82b3EzY2I5bjZzbzYybzlqNjFoajZvaHA2ZyBjeWJlcmp1bmtpZTA5QG0', 'sequence': 0, 'summary': 'Running', 'creator': {'email': 'cyberjunkie09@gmail.com', 'self': True, 'displayName': 'Brian Leeson'}, 'iCalUID': '64o6cob56tj62b9hckqm8b9k71h62b9o6oq3cb9n6so62o9j61hj6ohp6g@google.com', 'etag': '"2958492246350000"', 'reminders': {'overrides': [{'method': 'popup', 'minutes': 30}], 'useDefault': False}, 'end': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-11-16T07:00:00-08:00'}, 'created': '2016-11-15T21:42:03.000Z', 'status': 'confirmed'}]
  rangeStart = "2016-01-01T00:00:00-08:00"
  rangeEnd = "2016-01-01T23:59:00-08:00"
  result = [{'organizer': {'email': 'cyberjunkie09@gmail.com', 'self': True, 'displayName': 'Brian Leeson'}, 'kind': 'calendar#event', 'id': '64o6cob56tj62b9hckqm8b9k71h62b9o6oq3cb9n6so62o9j61hj6ohp6g', 'start': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-11-16T06:00:00-08:00'}, 'updated': '2016-11-15T21:42:03.235Z', 'htmlLink': 'https://www.google.com/calendar/event?eid=NjRvNmNvYjU2dGo2MmI5aGNrcW04YjlrNzFoNjJiOW82b3EzY2I5bjZzbzYybzlqNjFoajZvaHA2ZyBjeWJlcmp1bmtpZTA5QG0', 'sequence': 0, 'summary': 'Running', 'creator': {'email': 'cyberjunkie09@gmail.com', 'self': True, 'displayName': 'Brian Leeson'}, 'iCalUID': '64o6cob56tj62b9hckqm8b9k71h62b9o6oq3cb9n6so62o9j61hj6ohp6g@google.com', 'etag': '"2958492246350000"', 'reminders': {'overrides': [{'method': 'popup', 'minutes': 30}], 'useDefault': False}, 'end': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-11-16T07:00:00-08:00'}, 'created': '2016-11-15T21:42:03.000Z', 'status': 'confirmed'}]
  assert( relevantEvents(eventList, rangeStart, rangeEnd)== result)

  #Test 2 - null. no event
  eventList = []
  rangeStart = "2016-01-01T00:00:00-08:00"
  rangeEnd = "2016-01-01T23:59:00-08:00" 
  assert(relevantEvents(eventList, rangeStart, rangeEnd) == [] ) 
   
def test_groupByDay():

  #Test 1 - null. no events
  assert(groupByDay([])==[])

  #Test 2 - Single event
  bEvents = [['2016-11-16T06:00:00-08:00', '2016-11-16T07:00:00-08:00']]
  bGrouped = [[{'start': '2016-11-16T06:00:00-08:00', 'end': '2016-11-16T07:00:00-08:00'}]]
  assert(groupByDay(bEvents) == bGrouped)

  #Test 3 - Multiple days
  bEvents = [['2016-11-17T18:00:00-08:00', '2016-11-17T19:00:00-08:00'], ['2016-11-17T17:45:00-08:00', '2016-11-17T18:45:00-08:00'], ['2016-11-16T06:00:00-08:00', '2016-11-16T07:00:00-08:00']]
  bGrouped = [[{'end': '2016-11-16T07:00:00-08:00', 'start': '2016-11-16T06:00:00-08:00'}], [{'end': '2016-11-17T18:45:00-08:00', 'start': '2016-11-17T17:45:00-08:00'}, {'end': '2016-11-17T19:00:00-08:00', 'start': '2016-11-17T18:00:00-08:00'}]]
  assert(groupByDay(bEvents) == bGrouped)
  
def test_mergeBusy():

  #Test1 - multiple events. some needed merging
  gEvents = [[{'end': '2016-11-16T07:00:00-08:00', 'start': '2016-11-16T06:00:00-08:00'}], [{'end': '2016-11-17T18:45:00-08:00', 'start': '2016-11-17T17:45:00-08:00'}, {'end': '2016-11-17T19:00:00-08:00', 'start': '2016-11-17T18:00:00-08:00'}]]
  mBlocks = [[{'end': '2016-11-16T07:00:00-08:00', 'start': '2016-11-16T06:00:00-08:00', 'summary': 'Busy'}], [{'end': '2016-11-17T19:00:00-08:00', 'start': '2016-11-17T17:45:00-08:00', 'summary': 'Busy'}]]
  assert(mergeBusy(gEvents) == mBlocks)

  #Test2 - null. no events
  gEvents = []
  mBlocks = []
  assert(mergeBusy(gEvents) == mBlocks)


def test_addFree():
  #Test1 - null
  bBlocks = []
  sTime = "2016-01-01T00:00:00-08:00" 
  eTime = "2016-01-01T23:59:00-08:00" 
  sDate = "2016-11-17T00:00:00-08:00"
  eDate = "2016-11-18T00:00:00-08:00"
  fBSorted = [[{'end': '2016-11-17T23:59:00-08:00', 'start': '2016-11-17T00:00:00-08:00', 'summary': 'Free'}], [{'end': '2016-11-18T23:59:00-08:00', 'start': '2016-11-18T00:00:00-08:00', 'summary': 'Free'}]]
  assert(addFree(bBlocks, sTime, eTime, sDate, eDate) == fBSorted)

  #Test2 - single event
  bBlocks = [[{'end': '2016-11-17T19:00:00-08:00', 'start': '2016-11-17T18:00:00-08:00', 'summary': 'Busy'}]]
  sTime = "2016-01-01T00:00:00-08:00"
  eTime = "2016-01-01T23:59:00-08:00"
  sDate = "2016-11-17T00:00:00-08:00"
  eDate = "2016-11-18T00:00:00-08:00"
  fBSorted = [[{'end': '2016-11-17T18:00:00-08:00', 'start': '2016-11-17T00:00:00-08:00', 'summary': 'Free'}, {'end': '2016-11-17T19:00:00-08:00', 'start': '2016-11-17T18:00:00-08:00', 'summary': 'Busy'}, {'end': '2016-11-17T23:59:00-08:00', 'start': '2016-11-17T19:00:00-08:00', 'summary': 'Free'}], [{'end': '2016-11-18T23:59:00-08:00', 'start': '2016-11-18T00:00:00-08:00', 'summary': 'Free'}]]
  assert(addFree(bBlocks, sTime, eTime, sDate, eDate) == fBSorted)

  #Test3 - overlapping events
  bBlocks = [[{'end': '2016-11-17T19:00:00-08:00', 'start': '2016-11-17T17:45:00-08:00', 'summary': 'Busy'}], [{'end': '2016-11-18T17:00:00-08:00', 'start': '2016-11-18T16:00:00-08:00', 'summary': 'Busy'}]]
  sTime = "2016-01-01T00:00:00-08:00"
  eTime = "2016-01-01T23:59:00-08:00"
  sDate = "2016-11-17T00:00:00-08:00"
  eDate =  "2016-11-18T00:00:00-08:00"
  fBSorted = [[{'end': '2016-11-17T17:45:00-08:00', 'start': '2016-11-17T00:00:00-08:00', 'summary': 'Free'}, {'end': '2016-11-17T19:00:00-08:00', 'start': '2016-11-17T17:45:00-08:00', 'summary': 'Busy'}, {'end': '2016-11-17T23:59:00-08:00', 'start': '2016-11-17T19:00:00-08:00', 'summary': 'Free'}], [{'end': '2016-11-18T16:00:00-08:00', 'start': '2016-11-18T00:00:00-08:00', 'summary': 'Free'}, {'end': '2016-11-18T17:00:00-08:00', 'start': '2016-11-18T16:00:00-08:00', 'summary': 'Busy'}, {'end': '2016-11-18T23:59:00-08:00', 'start': '2016-11-18T17:00:00-08:00', 'summary': 'Free'}]]
  assert(addFree(bBlocks, sTime, eTime, sDate, eDate) == fBSorted)






