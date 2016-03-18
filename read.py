from firebase import firebase
#Class zone, used to save the data from all the zones
class Zone:
    number=0
    busy=0
    total=0
    def __init__(self,number,busy):
        self.number=number
        self.total=1
        if busy==0:
            self.busy=1
            
    def getNumber(self):
        return self.number
    
    def getBusy(self):
        return self.busy

    def setBusy(self,busy):
        self.busy=busy

    def increaseBusy(self):
        self.busy+=1

    def getTotal(self):
        return self.total

    def setTotal(self,total):
        self.total=total

    def increaseTotal(self):
        self.total+=1

    def printZone(self):
        print ("Zone: ",self.number,"\nTotal: ",self.total,"\nBusy: ",self.busy)
        

#this function is used to obtain data from the txt file
def obtainData():

    #opening the text file
    file=open("hi.csv","r")



    line=[] #includes all the lines in the file
    
    i=0
    text=file.readline()


    #reading the text file
    while text!="":
        line.append(text)
        line[i]=line[i].split(",")
        i+=1
        text=file.readline()

    file.close() #closing the file
    return line



#this function initializes the list of zone objects based on the line list
def initializeZones(line):
    zones=[] #includes the object of class zone
    zoneRef={} #dictionary to map letters to a number zone
    
    #initializing the zone list objects to None
    for x in range (len(line)):
        zones.append(None)

    keyCount=1 #the key used to represent a letter in the dictionary
    
    #Introducing the zones according to the list
    for x in line:
        
        if not(zoneRef.has_key(x[0])):
            zoneRef[x[0]]=keyCount
            keyCount+=1
        
        print (keyCount)
        
            
        if(zones[zoneRef[x[0]]]==None):
            zones[zoneRef[x[0]]]=Zone(zoneRef[x[0]],int(x[2]))
        else:
            zones[zoneRef[x[0]]].increaseTotal()

            if int(x[2])==0:
                       zones[zoneRef[x[0]]].increaseBusy()

    noneCount=0 #variable to count the number of nones
    for x in zones: #counting the None objects in the list
        if x==None:
            noneCount+=1

    for x in range(noneCount): #removing the nones in the list
        zones.remove(None)      

    return zones

#Updates the data of the zone to the database
def update(zone,firebase):
    url="ITESM/Zone"+str(zone.getNumber())
    #update busy and update total with zone.getBusy and zone.getTotal     
    firebase.patch(url,{"Busy":zone.getBusy()})
    firebase.patch(url,{"Total":zone.getTotal()})

    
line=obtainData()
zones=initializeZones(line)

firebase=firebase.FirebaseApplication("https://gubi.firebaseio.com",None)

for x in zones:
    update(x,firebase)





