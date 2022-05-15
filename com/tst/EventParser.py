# -*- coding:utf-8 -*-
'''
Created on 2022. febr. 24.

@author: MSzaba
'''
from datetime import datetime
from pathlib import Path
import random
import sys
import time

from bs4 import BeautifulSoup
from pythonwin.pywin.scintilla.control import null_byte
import requests
from unrpa.meta import description
from logging import _startTime

#from geopy.geocoders import Nominatim


fileOptionConst = "-f"
mandatoryPostfix = "?acontext=%7B%22event_action_history%22%3A[%7B%22surface%22%3A%22page%22%7D]%7D"
processedURLs = set()

processedEvents = {}

def UrlDownloader (url):
    session = requests.Session()
    session.trust_env = False

    headers = {
        #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39',
        'accept':    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #'accept-encoding':    'gzip, deflate, br',
        'accept-language':    'en-US,en;q=0.9',
        'cache-control':    'max-age=0',
        'sec-ch-ua':    '" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
        'sec-ch-ua-mobile':    '?0',
        'sec-ch-ua-platform':    '"Windows"',
        'sec-fetch-dest':    'document',
        'sec-fetch-mode':   'navigate',
        'sec-fetch-site':    'none',
        'sec-fetch-user':    '?1',
        'upgrade-insecure-requests':   '1'
    }
    print("--------------------------------")
    print("Processing event: " + url)

    r = session.get(url, headers = headers)
    #print( "URL loaded. ")
    retVal = str(r.content);
    return retVal

def ParseFile(content1):
    soup = BeautifulSoup(content1, features="html.parser")
    #print( "URL parsed. ")
    return soup.prettify()
    return soup

def FileWriter(content2, prefix):
    time.sleep(1)
    today = datetime.now()
    ext = today.strftime("%y_%m_%d_%H_%M_%S")
    
    f = open("C:\\tmp2\\" +prefix +"_" + ext + ".txt", "x")
    #soup = BeautifulSoup(content2, features="html.parser")
    #converted = str(soup.string)
    #converted2 = converted.replace('\n', '')
    content3 = content2.replace('\n', '')
    f.write(content3)
    f.flush()
    f.close()
    #print("File is written")
    
    
def getTitle(content):
    soup = BeautifulSoup(content, features="html.parser")
    elements = soup.find_all("title")
    if elements is None:
        print("Title was not found")
        return None
    else:
        for element in elements:
            elementString = str(element)
            endIndex = len(elementString) - 8
            title = elementString[8:endIndex]
            #print("original Title: " + title)
            #print("Title: " + bytes(title, "utf-8").decode())
            encoded = title.encode("latin1")

            removed = removeExtraSlash(encoded)
            
            try:
                reDecoded = removed.decode("utf-8")
            except UnicodeDecodeError:
                print("String transformation was not successful. Another way is started")
                print("original Title: " + title)
                reDecoded = unicodeTransformerSlashX(str(title))

            
            #print("Title: " , reDecoded)
            return reDecoded
        
def unicodeTransformerSlashX(target):
    dictionary = {
        "\\xc3\\xb3": "ó",
        "\\xc5\\x91": "ő",
        "\\xc3\\xb6": "ö",
        "\\\\u00f6": "ö",
        "\\\\u0151": "ő",
        "\\xc3\\xa9": "é",
        "\\\\u00ed": "í",
        "\\xc3\\xa1": "á",
        "\\\\u00fc": "ü",
        "\\\\u0171": "ű",
        "\\\\u00fa": "ú",
        "\\\\u00c9": "É",
        "\\\\u00cd": "Í",
        "\\\\u00d3": "Ó",
        "\\\\u00c1": "Á",
        "\\\\u00d6": "Ö",
        "\\\\u00da": "Ú",
        "\\\\u00dc": "Ü",
        "\\\\u0150": "Ő",
        "\\n": " ",
        "\\\\u27a4": "➤",
        "\\\\ud83c": "",
        "\\\\udfab": "",
        "\\\\ud83d": "",
        "\\\\ude42": "",
        "\\\\ud83e": "",
        "\\\\udd18": "",
        "\\\\ud83e": "",
        "\\\\udd86": "",
        "\\\\u201c": "",
        "\\\\u201d": "",
        "\\\\u0040": "@",
        "\/u00ab": "",
        "\/u00bb": "",
        "\\xe2\\x80\\x93": "",
        "\\xe2\\x98\\qx85": "★",
        "\\/": "\\"
    }
    result = target
    for key in dictionary:
        result = result.replace(key, dictionary[key])
    return result
        
def removeExtraSlash(textToProcess):
    #return str(textToProcess).replace("\\\\", "\\")
    #textToProcess = []
    #textToProcess[:] = param
    to_remove = []
    to_modif = []
    for i in range(0, len(textToProcess) - 3):
        if  textToProcess[i] == 92 and textToProcess[i + 1] == 120 and textToProcess[i + 4] == 92 and textToProcess[i + 5] == 120:
            to_remove.append(i)
            cc = chr(int(ascii(textToProcess[i + 2]))) + chr(int(ascii(textToProcess[i + 3]))) + chr(int(ascii(textToProcess[i + 6]))) + chr(int(ascii(textToProcess[i + 7])))
            to_modif.append(bytearray.fromhex(cc))
    to_remove.reverse()
    for i in to_remove:
        textToProcess=textToProcess[:i] + to_modif.pop() + textToProcess[(i+8):]
    return textToProcess

def getDetailSection(parsed):
    sectionStart = "__module_component_EventCometContextRowMemberAttendance_event"
    sectionEnd = "</script>"
    stringRepresentation = str(parsed)
    startIndex = stringRepresentation.find(sectionStart)
    if startIndex < 0:
        checkLoginForm(parsed)
        return None
    endIndex = stringRepresentation.find(sectionEnd, startIndex);
    if endIndex < 0:
        return None
    part = stringRepresentation[startIndex:endIndex]
    print("Detail found and saved: ")
    FileWriter(part, "eventDetails")
    return part

def checkLoginForm(parsed):
    passTag = "pass"
    emailTag = "email"
    if parsed.find(passTag) > 0 and parsed.find(emailTag) > 0:
        print("Login screeen is displayed")
    
def getDescription(text):
    startText = 'event_description":{"text":"'
    startIndex = text.find(startText)
    if startIndex < 0:
        return None
    endIndex = text.find('"', startIndex + len(startText))
    if endIndex < 0:
        return None
    actualStartIndex = startIndex + len(startText)
    description = text[actualStartIndex:endIndex]
    #converted = ''.join(chr(ord(c)) for c in description)
    #udata=description.decode("utf-8")
    #converted=udata.encode("ascii","ignore")
    #converted = description.encode('ascii', 'ignore')
    #print("Original description: " , description)
    #removed1 = removeExtraSlash(description)
    #print("removed: ", removed1)
    
    #encoded = removed1.encode("latin1")

 #   removed = removeExtraSlash(encoded)
  #  print("removed: ", removed)

#    reDecoded = removed.decode("utf-8")
    reDecoded = unicodeTransformer(description)
    
    #print("description: " + reDecoded)
    return reDecoded


def unicodeTransformer(target):
    dictionary = {
        "\\\\u00f3": "ó",
        "\\\\u00f6": "ö",
        "\\\\u0151": "ő",
        "\\\\u00e9": "é",
        "\\\\u00ed": "í",
        "\\\\u00e1": "á",
        "\\\\u00fc": "ü",
        "\\\\u0171": "ű",
        "\\\\u00fa": "ú",
        "\\\\u00c9": "É",
        "\\\\u00cd": "Í",
        "\\\\u00d3": "Ó",
        "\\\\u00c1": "Á",
        "\\\\u00d6": "Ö",
        "\\\\u00da": "Ú",
        "\\\\u00dc": "Ü",
        "\\\\u0150": "Ő",
        "\\\\n": " ",
        "\\\\u27a4": "➤",
        "\\xe2\\x98\\qx85": "★",
        "\\\\ud83c": "",
        "\\\\udfab": "",
        "\\\\ud83d": "",
        "\\\\ude42": "",
        "\\\\ud83e": "",
        "\\\\udd18": "",
        "\\\\ud83e": "",
        "\\\\udd86": "",
        "\\\\u201c": "",
        "\\\\u201d": "",
        "\\\\u0040": "@",
        "\\\\u2019": "'",
        "\\\\u2736": '✶',
        "\\\\udfb7": "",
        "\\\\udcaf": "",
        "\\\\udc4c": "",
        "\/u00ab": "",
        "\/u00bb": "",
        "\\/": "\\",
        "\\\\": "/"
    }
    result = target
    for key in dictionary:
        result = result.replace(key, dictionary[key])
    return result

def getLocation(detailSection):
    
    locationSegment = getLocationSegment(detailSection)
    if locationSegment is not None:
            #print("Segment:" , locationSegment)
            locationName = getLocationName(locationSegment)
            address = getAddress(locationSegment)
            transformedName = unicodeTransformer(locationName)
            locationData = {
                "name": transformedName,
                "address": address
            }
            #print("location: ", transformedName, " ", address )
            return locationData
        
def getLocationName(locationSegment):
    startText = 'Page","contextual_name":"'
    startIndex = locationSegment.find(startText)
    if startIndex < 0:
        startText = '"contextual_name":"'
        startIndex = locationSegment.find(startText)
        if startIndex < 0:
            return ""
    endIndex = locationSegment.find('"', startIndex + len(startText))
    if endIndex < 0:
        return ""
    return locationSegment[startIndex + len(startText):endIndex]

def getAddress(locationSegment):
    startText = 'address":{"street":"'
    startIndex = locationSegment.find(startText)
    if startIndex < 0:
        return checkLatitudeLocation(locationSegment)
    endIndex = locationSegment.find('"', startIndex + len(startText))
    if endIndex < 0:
        return ""
    streetAddress = locationSegment[startIndex + len(startText):endIndex]
    startCityText = 'city":{"contextual_name":"'
    startCityIndex = locationSegment.find(startCityText)
    if startCityIndex < 0:
        return ""
    endCityIndex = locationSegment.find('"', startCityIndex + len(startCityText))
    if endCityIndex < 0:
        return ""
    cityAddress = locationSegment[startCityIndex + len(startCityText):endCityIndex]
    
    return unicodeTransformer(cityAddress + " " + streetAddress)
    
    
def checkLatitudeLocation(locationSegment):
    startText = 'latitude":'
    startIndex = locationSegment.find(startText)
    if startIndex < 0:
        return ""
    endIndex = locationSegment.find(',', startIndex + len(startText))
    latitude = locationSegment[startIndex + len(startText):endIndex]
    startText = 'longitude":'
    startIndex = locationSegment.find(startText)
    if startIndex < 0:
        return ""
    endIndex = locationSegment.find('}', startIndex + len(startText))
    longitude = locationSegment[startIndex + len(startText):endIndex]
    
    #geolocator = Nominatim(user_agent="specify_your_app_name_here")
    #location = geolocator.reverse("52.509669, 13.376294")
    #print(location.address)
    return latitude + ", " + longitude
    
def getLocationSegment(detailSection):
    startText = 'event_place":{"'
    openingBracket = '{'
    closingBracket = '}'
    nrOfOpenBrackets = 0
    startIndex = detailSection.find(startText)
    if startIndex < 0:
        return None
    selectedText = detailSection[startIndex + len(startText):]
    for i in range(len(selectedText)):
        if selectedText[i] == closingBracket:
            if nrOfOpenBrackets == 0:
                return selectedText[:i]
            else:
                nrOfOpenBrackets = nrOfOpenBrackets -1
        if selectedText[i] == openingBracket:
            nrOfOpenBrackets = nrOfOpenBrackets + 1
  
def getStartTieme(parsed):
    startText = 'day_time_sentence":"'
    startIndex = parsed.find(startText)
    if startIndex < 0:
        return None
    endIndex = parsed.find('"', startIndex + len(startText))
    if endIndex < 0:
        return ""
    startTime = parsed[startIndex + len(startText):endIndex]
    return unicodeTransformer(startTime)
    
def getEventHosts(parsed):
    segment = getEventHostSegment(parsed)
    if segment is not None:
        listOfHosts = getHostLists(segment)
        if listOfHosts is not None and len(listOfHosts) > 0:
            hostNames = getHostNames(listOfHosts)
            return hostNames
        else:
            print("unable to find event hosts")
    else:
        print("unable to find event hosts description")
    return None

def getEventHostSegment(parsed):
    startText = 'event_hosts_that_can_view_guestlist":['
    startIndex = parsed.find(startText)
    if startIndex < 0:
        return None
    endIndex = parsed.find(']', startIndex + len(startText))
    if endIndex < 0:
        return ""
    listItems = parsed[startIndex + len(startText):endIndex]
    #print("Event list segment: " , listItems)
    return listItems


def getHostLists(segment):
    hostList = set()
    openingBracket = '{'
    closingBracket = '}'
    nrOfOpenBrackets = 0
    previousStartIndex = 0
    isHostInProcess = False
    
    for i in range(len(segment)):
        if segment[i] == closingBracket:
            #print("closing bracket at " , i)
            if nrOfOpenBrackets == 1: 
                newSegment = segment[previousStartIndex:i]
                #print("Add a new segment: " , newSegment)
                hostList.add(newSegment)
                isHostInProcess = False
                nrOfOpenBrackets = nrOfOpenBrackets -1
            else:
                nrOfOpenBrackets = nrOfOpenBrackets -1
        if segment[i] == openingBracket:
            #print("open bracket at " , i)
            nrOfOpenBrackets = nrOfOpenBrackets + 1
            if not isHostInProcess:
                isHostInProcess = True
                previousStartIndex = i
    #print("Host List:" , hostList)
    return hostList
   
def getHostNames(listOfHosts):
    hostNames  = set()
    for segment in listOfHosts:
        #print("segment: " , segment)
        startText = '"name":"'
        startIndex = segment.find(startText)
        if startIndex < 0:
            continue
        endIndex = segment.find('"', startIndex + len(startText))
        if endIndex < 0:
            continue
        name = segment[startIndex + len(startText):endIndex]
        hostNames.add(unicodeTransformer(name))
    return hostNames

def processUrl(url):
    url = addMandatoryPostfix(url.strip()).strip()
    if url in processedURLs:
        print("Url is already processed: ", url)
        return
    content = UrlDownloader(url)
    parsed = ParseFile(content)
    #FileWriter(parsed.decode(pretty_print=True))
    #FileWriter(parsed.encode("utf-8").decode())
    FileWriter(str(parsed.encode('utf8')), "eventContnet")
    title = getTitle(parsed)
    detailSection = getDetailSection(parsed)
    description = ""
    location = ""
    if detailSection is None:
        print("unable to find event details, the access might be blocked")
    else:
        description = getDescription(detailSection)
        location = getLocation(detailSection)
    startTime = getStartTieme(parsed)
    #print("Start time: " , startTime)
    eventHosts = getEventHosts(parsed)
    #print("Host names: " , eventHosts)
    printEventDetails(title,description,location,startTime,eventHosts)
    addProcessInfoToSet(location,startTime,eventHosts)
    #print("URL has added to the visited list")
    processedURLs.add(url)
    
    
def addMandatoryPostfix(url):
    if not url.strip().endswith(mandatoryPostfix):
        print("append mandatory postfix to url")
        url = url.strip() +mandatoryPostfix
    return url
    
    
def printEventDetails(title,description,location,startTime,eventHosts):
    print("----------------------------------")
    if eventHosts is not None and location is not None:
        print(f"{eventHosts} @ {location} ({startTime}) [{title}] | {description}")
    if eventHosts is not None and location is None:
        print(f"{eventHosts} @ ({startTime}) [{title}] | {description}")
    else:
        print("Event cannot be processed")

#url= "https://www.facebook.com/events/660291668647135/?ref=newsfeed&__cft__[0]=AZXrA8ucQnHtsARxHfdny1ayHdr3IqsEPHIX1klNqvzUOpNhk1Or2ujAWIIrUVy_XUprabtTChyzKYl-cvMYFo7P7_Qunctpqv8zEYGtcPiIh_YeotPWAcgvs2RshmZCgrQpXZYhhpOR1JLUNMAXym2tmFRHEE3cx-Co6KnZiRRKOF73wDueSFK3C2xmlPLXxPU&__tn__=H-R"
#url= "https://www.facebook.com/events/484279216489566/?acontext=%7B%22event_action_history%22%3A[%7B%22extra_data%22%3A%22%22%2C%22mechanism%22%3A%22your_upcoming_events_unit%22%2C%22surface%22%3A%22bookmark%22%7D%2C%7B%22extra_data%22%3A%22%22%2C%22mechanism%22%3A%22your_upcoming_events_unit%22%2C%22surface%22%3A%22bookmark%22%7D]%2C%22ref_notif_type%22%3Anull%7D"
#url= "https://www.facebook.com/events/499205238321110/"
#url= "https://www.facebook.com/events/217414153851337/"

def getInputParameters():
    #print("input parameters: " ,sys.argv)
    inputParameters = list()
    if len(sys.argv) == 2:
        inputParameters.append(sys.argv[1])
        return inputParameters
    if len(sys.argv) == 3 and sys.argv[1] == fileOptionConst:
        inputParameters.append(fileOptionConst)
        inputParameters.append(sys.argv[2])
        return inputParameters
    print("Unknown or missing input parameters")
    print("Use a FB event URL to process as parameter.")
    print("Or use -f option and enter a filename with URLs.")
    quit()

def checkInputParameters(inputParameters):
    if len(inputParameters) == 1:
        return False
    return True

def loadURLList(fileName):
    path = Path(fileName)
    if path.is_file():
        lines = []
        with open(path) as f:
            lines = f.readlines()
            return lines
    else:
        print("Unable to reach file: ", fileName)
        return None
    
def Wait():
    time.sleep(random.randint(2300, 4350)/1000)

def createProcessedEventsDictionary():
    retVal = {}
    retVal["Thursday"] = createSubDictionary()
    retVal["Friday"] = createSubDictionary()
    retVal["Saturday"] = createSubDictionary()
    retVal["Sunday"] = createSubDictionary()
    retVal["Monday"] = createSubDictionary()
    retVal["Tuesday"] = createSubDictionary()
    retVal["Wednesday"] = createSubDictionary()
    return retVal
    
def createSubDictionary():
    retVal = {}
    retVal["Budapest"] =[]
    retVal["Vidék"] =[]
    retVal["Külföld"] =[]
    retVal["Média"] =[]
    retVal["Média"] =[]
    return retVal

def addProcessInfoToSet(location,startTime,eventHosts):
    print("eventHost", eventHosts)
    print("location", location)
    print("startTime", startTime)
    venueToPrint = ""
    if location is not None and  len(location) > 0:
        venueToPrint = location["name"]
    hostToPrint = ""
    if eventHosts is not None:
        for host in eventHosts:
            if venueToPrint != host:
                hostToPrint = hostToPrint + host + " "
    city = ""
    if location is not None and len(location) > 0 and location["address"] is not None and len(location["address"]) > 0:
        splitted = location["address"].split()
        city = splitted[0]
    day = ""
    startTimeAsString = ""
    if startTime is not None:
        splitted = startTime.split(",")
        day = splitted[0] 
        startTimeAsString = "unknown"
        locationOfAT = startTime.find("at ")
        if locationOfAT > 0:
            startTimeAsString = startTime[locationOfAT:].split()[1].strip()
            
    
    if day is not None and len(day) > 0:
        if day not in processedEvents or processedEvents[day] is None:
            processedEvents[day] = []
        record = {
            "band": hostToPrint,
            "venue": venueToPrint,
            "city": city,
            "startTime":  startTimeAsString
            }
        processedEvents[day].append(record)
    print("eventHost", hostToPrint)
    print("location", venueToPrint)
    print("city", city)
    print("day", day)
    print("Start Time: ",startTimeAsString)

def printSummarizedData():
    print("----------Summarized format-----------")
    if len(processedEvents) > 0:
        print()
        #print(processedEvents)
        for day in processedEvents:
            print("Day: " , day)
            if len(day) > 0:
                
                for group in processedEvents[day]:
                    #print(group)
                    band = group["band"]
                    location = group["venue"]
                    city = group["city"]
                    startTime = group["startTime"]
                    print(f"{band} @ {location} {startTime} ({city})")
                print()
    

processedEvents = {}
inputParameters = getInputParameters() 
if  inputParameters is not None and len(inputParameters) > 0:
    print("input parameters: " ,inputParameters)
    print("--------------------------------")
    isFileShouldBeProcessed = checkInputParameters(inputParameters)
    if isFileShouldBeProcessed is not None:
        if isFileShouldBeProcessed:
            fileName = inputParameters[1]
            if fileName is not None:
                listOfURLs = loadURLList(fileName)
                for url in listOfURLs:
                    #print("url: ", url)
                    if url is None:
                        continue
                    if len(url.strip()) == 0:
                        continue
                    if url.strip() == "#":
                        print("Break character (#) was reached. Stop processing")
                        break
                    processUrl(url)
                    Wait()
        else:
            processUrl(inputParameters[0])   
        printSummarizedData()   
    else:
        print("Unable to process input parameters")
else:
    print("Input parameter is required.")
    print("Use a FB event URL to process as parameter.")
    print("Or use -f option and enter a filename with URLs.")






if __name__ == '__main__':
    pass