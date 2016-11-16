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
  
  #sort all events by start time
  busySorted = sorted(busyEvents, key=lambda event: event[0]) 
  
  """
  print("should be sorted")
  for event in busySorted:
    print("event start is:", event[0]) 
  """

  #group by day
  busySorted.append("$") #append dummy
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

  return busyGrouped


def mergeBusy(groupedEvents):
  """
  events = dict
  args: a list of lists of events
  ret: a list of lists of events, that have over lapping events merged
    Events will contain only {"start": startTime, "end": endTime, AND "summary" : "busy"}
  """
    
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
 
def addFree(busyBlocks, startRange, endRange):
  """
  args: busyBlocks: list of list of dicts. List of days of blocks. Each block has a start, end, and summary field
        startRange/endRange: iso formated strings representing start and end times
  ret: list of list of dict. adds "free times" and blocks, "summary": "free".
  """
  #TODO

  freeBusyList = []
 
  for days in busyBlocks:
    #handle the year, mo, day not being this days' YMD
    #print("first block:", days[0]["start"])
    mold = arrow.get(days[0]["start"]) 
    startRange = arrow.get(startRange).replace(year=mold.year, month=mold.month, day=mold.day).isoformat()
    endRange = arrow.get(endRange).replace(year=mold.year, month=mold.month, day=mold.day).isoformat()

    dayBlocks = []
    #if the first event starts after the start of the range, make free block
    if (startRange < days[0]["start"]):
      block = {"start": startRange, "end": days[0]["start"], "summary": "Free"}
      dayBlocks.append(block)

    for i in range(len(days)-1):
      #blocks cannot overlap. get end time of ith block, start time of ith+1 block
      block = {"start": days[i]["end"],"end": days[i+1]["start"], "summary": "Free"}
      dayBlocks.append(block)

    #if the last event ends before the end of the range, make free block
    #print("bool:", (endRange > days[-1]["end"]))
    #print("eR:", endRange)
    #print("last item endTime:", days[-1]["end"])
    if (endRange > days[-1]["end"]):
      block = {"start": days[-1]["end"], "end": endRange, "summary": "Free"}
      dayBlocks.append(block) 
    
    dayBlocks.extend(days)
    freeBusyList.append(dayBlocks)   


  freeBusySorted = []
  #sort by start time
  for day in freeBusyList:
    daySorted = sorted(day, key=lambda event: event["start"])
    freeBusySorted.append(daySorted)

  
  print("freeBusyList")
  for item in freeBusySorted:
    print("item:", item)
  

  return freeBusySorted




