import arrow

def relevantEvents(eventList, rangeStart, rangeEnd):
  """
  arg: a dictionary of events, 
    range start time as string
    range end time as string
  return: list of relevant events
    list = [summary,
            startTime,
            endTime]
  Credit: Sam Oberg helped with the logic for this function
  """
  """
  print("eventList is:", eventList)
  print("rangeStart is:", rangeStart)
  print("rangeEnd is:", rangeEnd)
  """
  inRangeEvents = []
  for event in eventList:
    #print("event is:", event)
    if "gadget" in event:
      continue
    if "transparency" in event:
      continue
    if arrow.get(event["end"]["dateTime"]).timetz() < arrow.get(rangeStart).timetz():
      continue
    if arrow.get(event["start"]["dateTime"]).timetz() > arrow.get(rangeEnd).timetz():
      continue 
    else:
      inRangeEvents.append(event)
      #print("event start is:", event["start"])

  #print("inRangeEvents is:", inRangeEvents)
  return inRangeEvents

def groupByDay(busyEvents):
  """
  args: takes a list of busy events
  ret: list of list of busy events
    where each item is a day and in each day events are sorted by start time.
  Notes:
    Strips event data. Each event only has start and end keys
  Example:
    [[{e1},{e2},{e3}], [{},{},{}], ..., [...]]  
  """
  #print("busyEvents is:", busyEvents)  


  #sort all events by start time
  busySorted = sorted(busyEvents, key=lambda event: event[0]) 
  
  """
  print("should be sorted")
  for event in busySorted:
    print("event start is:", event[0]) 
  """

  #group by day
  busySorted.append("$") #append sentinel
  busyGrouped = []
  dayGroup = []
  for i in range(len(busySorted)-1):
    if (busySorted[i+1] == "$"): #if done break
      event  = {"start": busySorted[i][0], "end": busySorted[i][1]}
      dayGroup.append(event)
      busyGrouped.append(dayGroup)
      break
      
    #stip down event
    event  = {"start": busySorted[i][0], "end": busySorted[i][1]}
    #add it to the day
    dayGroup.append(event)
    
    #if it's day is different from the next day, append dGroup, dGroup =[]
    if (arrow.get(busySorted[i][0]).day != arrow.get(busySorted[i+1][0]).day):
      busyGrouped.append(dayGroup)
      dayGroup = []
  
  """
  print("busyGrouped is:", busyGrouped)
  for day in busyGrouped:
    print("day")
    for event in day:
      print("event start", event["start"])
  """
  #print("busyGrouped is:", busyGrouped)
  return busyGrouped


def mergeBusy(groupedEvents):
  """
  events = dict
  args: a list of lists of events
  ret: a list of lists of events, that have over lapping events merged
    Events will contain only {"start": startTime, "end": endTime, AND "summary" : "busy"}
  """
  #print("groupedEvents is:", groupedEvents)  
  mergedBlocks = []  #going to be a list of lists of dicts/busy blocks
  for day in groupedEvents:
    mergedDays = []
    day.append("$") #append dummy

    for i in range(len(day)- 1):
      #start/end of ith event
      startTime = day[i]["start"]
      endTime = day[i]["end"]
    
      if (day[i+1] == "$"):  #if at end, break
        block = {"start": startTime, "end": endTime, "summary": "Busy"}
        mergedDays.append(block)
        break
      
      startTimeNext = day[i+1]["start"]
      endTimeNext = day[i+1]["end"]
      
      #OVERLAPPING
      #if end of i > start i+1, event is overlapping group the events, place at i+1
      if (endTime >  startTimeNext):
        day[i+1] = {"start": startTime, "end": endTimeNext}

      #NON OVERLAPPING
      #else we've found a non overlapping event, add event as a busy block
      else:
        block = {"start": startTime, "end": endTime, "summary": "Busy"}
        mergedDays.append(block)

    mergedBlocks.append(mergedDays) #append the days blocks
    
  #print("mergedBlocks is:", mergedBlocks)
  return mergedBlocks
 
def addFree(busyBlocks, startTime, endTime, startDate, endDate):
  """
  args: busyBlocks: list of list of dicts. List of days of blocks. Each block has a start, end, and summary field
        startRange/endRange: iso formated strings representing start and end times
  ret: list of list of dict. adds "free times" and blocks, "summary": "free".
  """
  #print("busyBlocks is:", busyBlocks)
  #print("startRange is", startRange)
  #print("endRange is:", endRange)
  freeBusyList = []

  #find how many days we are covering
  startDate = arrow.get(startDate)
  endDate = arrow.get(endDate).replace(days=+1) #include final day
  diff = endDate.day - startDate.day
 
  ithStart = startDate.replace(hour=arrow.get(startTime).hour, minute=arrow.get(startTime).minute)  
  ithEnd = startDate.replace(hour=arrow.get(endTime).hour, minute=arrow.get(endTime).minute) 

  dayIndex = 0
  bbIndex = 0
  freeBusyList = []
  bbDay = arrow.get(busyBlocks[bbIndex][0]["start"])
  
  while(dayIndex<diff):
    dayBlocks = [] 
    bbDay = arrow.get(busyBlocks[bbIndex][0]["start"])
    #Case: day has no events
    #if currDay != ith day: make free block of day
    if (bbDay.date() != ithStart.date()): #found clear day
      print("found clear day")
      
      block = {"start": ithStart.isoformat(), "end": ithEnd.isoformat(), "summary": "Free"}
      dayBlocks.append(block)
    
    #Else: has has events
    else:
      day = busyBlocks[bbIndex]
   
      #Case: start of day
      if (day[0]["start"] > ithStart.isoformat()):
        block = {"start": ithStart.isoformat(), "end": day[0]["start"], "summary": "Free"}
        dayBlocks.append(block)

      #Case: middle of day. loop over event in the day
      for i in range(len(day)-1):
        #blocks cannot overlap. get end time of ith block, start time of ith+1 block
        block = {"start": day[i]["end"],"end": day[i+1]["start"], "summary": "Free"}
        dayBlocks.append(block)

      #Case: end of day
      if (day[0]["end"] < ithEnd.isoformat()):
        block = {"start": day[0]["end"], "end": ithEnd.isoformat(), "summary": "Free"}
        dayBlocks.append(block)
      
      dayBlocks.extend(day)
      #if we've processed a day, increment the day counter
      if (bbIndex < len(busyBlocks)-1):
        bbIndex+=1
        bbDay = arrow.get(busyBlocks[bbIndex][0]["start"])

    #increment ithStart/ithEnd and day index
    ithStart = ithStart.replace(days=+1)
    ithEnd = ithEnd.replace(days=+1)
    dayIndex+=1
    freeBusyList.append(dayBlocks)
 
  freeBusySorted = []
  #sort by start time
  for day in freeBusyList:
    daySorted = sorted(day, key=lambda event: event["start"])
    freeBusySorted.append(daySorted)

  """
  print("freeBusyList")
  for item in freeBusySorted:
    print("item:", item)
  """
  #print("freeBusySorted:", freeBusySorted)
  return freeBusySorted




