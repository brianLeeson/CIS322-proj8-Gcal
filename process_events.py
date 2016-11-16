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
    if "transparency" in event:
      continue
    if arrow.get(event["end"]["dateTime"]).timetz() < arrow.get(rangeStart).timetz():
      continue
    if arrow.get(event["start"]["dateTime"]).timetz() > arrow.get(rangeEnd).timetz():
      continue 
    else:
      inRangeEvents.append(event)
      print("event start is:", event["start"])
  return inRangeEvents

def groupByDay(busyEvents):
  """
  args: takes a list of busy events
  ret: list of list of busy events
    where each item is a day and in each day events are sorted by start time
  Example:
    [[{e1},{e2},{e3}], [{},{},{}], ..., [...]]  
  """
  
  #sort all events by start time
  busySorted = sorted(busyEvents, key=lambda event: event["start"]["dateTime"])
  
  """  
  print("should be sorted")
  for event in busySorted:
    print("event start is:", event["start"]["dateTime"]) 
  """

  #group by day
  busySorted.append("$") #append dummy
  busyGrouped = []
  dayGroup = []
  for i in range(len(busySorted)-1):
    if (busySorted[i+1] == "$"): #if done break
      dayGroup.append(busySorted[i])
      busyGrouped.append(dayGroup)
      break
      
    #add it to the day
    dayGroup.append(busySorted[i])
    
    #if it's day is different from the next day, append dGroup, dGroup =[]
    if (arrow.get(busySorted[i]["start"]["dateTime"]).day != arrow.get(busySorted[i+1]["start"]["dateTime"]).day):
      busyGrouped.append(dayGroup)
      dayGroup = []
  """
  print("busyGrouped is:")
  for day in busyGrouped:
    print("day")
    for event in day:
      print("event summary", event["summary"])
  """

  return busyGrouped


def mergeBusy(busyEvents):
  """
  events = dict
  args: a list of lists of events
  ret: a list of lists of events, that have over lapping events merged
    Because of this merging, events will contain only startTime and endTime
  """
  #TODO

  return busyEvents
 
def addFree(busyBlocks):
  """
   
  """
  #TODO
  return busyBlocks




