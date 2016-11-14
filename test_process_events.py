from process_events import process

def test_process():
  
  #Test 1 - normal. 1 event provided, 1 event created
  eventList = [{'iCalUID': 'vv0pm3po9mbr4ggnvgvgh76pv8@google.com', 'reminders': {'useDefault': True}, 'updated': '2016-10-14T01:11:07.428Z', 'creator': {'displayName': 'Brian Leeson', 'email': 'cyberjunkie09@gmail.com', 'self': True}, 'id': 'vv0pm3po9mbr4ggnvgvgh76pv8', 'htmlLink': 'https://www.google.com/calendar/event?eid=dnYwcG0zcG85bWJyNGdnbnZndmdoNzZwdjhfMjAxNjEwMDdUMDEwMDAwWiBjeWJlcmp1bmtpZTA5QG0', 'start': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-10-06T18:00:00-07:00'}, 'status': 'confirmed', 'recurrence': ['RRULE:FREQ=WEEKLY;WKST=MO;COUNT=10;BYDAY=TH'], 'kind': 'calendar#event', 'sequence': 1, 'etag': '"2952814934856000"', 'end': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-10-06T19:00:00-07:00'}, 'created': '2016-10-05T23:17:40.000Z', 'organizer': {'displayName': 'Brian Leeson', 'email': 'cyberjunkie09@gmail.com', 'self': True}, 'summary': 'Dev Club'}]
  rangeStart = "2016-01-01T00:00:00-08:00"
  rangeEnd = "2016-01-01T23:59:00-08:00"
  assert( process(eventList, rangeStart, rangeEnd)== [{'eventEnd': '19:00:00', 'summary': 'Dev Club', 'eventStart': '18:00:00'}])

  #Test 2 - null. no event
  eventList = []
  rangeStart = "2016-01-01T00:00:00-08:00"
  rangeEnd = "2016-01-01T23:59:00-08:00" 
  assert( process(eventList, rangeStart, rangeEnd) == [] ) 

  #Test 3 - out of range. event provided out of range
  eventList = [{'recurrence': ['RRULE:FREQ=WEEKLY;WKST=MO;COUNT=10;BYDAY=TH'], 'iCalUID': 'vv0pm3po9mbr4ggnvgvgh76pv8@google.com', 'id': 'vv0pm3po9mbr4ggnvgvgh76pv8', 'end': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-10-06T19:00:00-07:00'}, 'creator': {'email': 'cyberjunkie09@gmail.com', 'displayName': 'Brian Leeson', 'self': True}, 'kind': 'calendar#event', 'summary': 'Dev Club', 'status': 'confirmed', 'sequence': 1, 'updated': '2016-10-14T01:11:07.428Z', 'organizer': {'email': 'cyberjunkie09@gmail.com', 'displayName': 'Brian Leeson', 'self': True}, 'htmlLink': 'https://www.google.com/calendar/event?eid=dnYwcG0zcG85bWJyNGdnbnZndmdoNzZwdjhfMjAxNjEwMDdUMDEwMDAwWiBjeWJlcmp1bmtpZTA5QG0', 'reminders': {'useDefault': True}, 'etag': '"2952814934856000"', 'start': {'timeZone': 'America/Los_Angeles', 'dateTime': '2016-10-06T18:00:00-07:00'}, 'created': '2016-10-05T23:17:40.000Z'}]
  rangeStart = "2016-01-01T00:00:00-08:00"
  rangeEnd = "2016-01-01T11:59:00-08:00"
  assert(process(eventList, rangeStart, rangeEnd) == [])

