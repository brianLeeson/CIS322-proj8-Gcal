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
      #print("event is:", event)
  return inRangeEvents

def groupByDay(busyEvents):
  """
  args: takes a list of busy events
  ret: list of list of busy events
    where each item is a day and in each day events are sorted by start time
  Example:
    [[{e1},{e2},{e3}], [{},{},{}], ..., [...]]  
  """
  
  #group by day



  #sort each day by start time



  return busyEvents


def mergeBusy(busyEvents):
  """
  args: a list of lists
  """
  #TODO
  return busyEvents
 
def addFree(busyBlocks):
  """
   
  """
  #TODO
  return busyBlocks




