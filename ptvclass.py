from hashlib import sha1
import hmac
import requests
import datetime

class PTVAPIClass():
    """A wrapper for the Melbourne PTV API"""

    def __init__(self, devid, key):
        """
        Pass in detail record from infile on creation
        Input:
        devid, key - developer ID and Key provided by PTV
        """
        self.devid = devid
        self.key = key
        self.routes = {}
        self.age = datetime.datetime.now()
        # Refresh lines to build initial train line data
        self.refreshlines()
        
        
    def getsigurl(self, request):
        # Define constants for request url
        baseurl = 'http://timetableapi.ptv.vic.gov.au'

        request = request + ('&' if ('?' in request) else '?')
        raw = request + 'devid={}'.format(self.devid)
        hashed = hmac.new(self.key.encode('utf-8'), raw.encode('utf-8'), sha1)
        sig = hashed.hexdigest()

        # Return a workable url
        return baseurl + raw + '&signature={}'.format(sig)


    def refreshlines(self):
        # Request to PTV API
        r = requests.get(self.getsigurl(self.selecturl('refresh')))
        jsonout = r.json()

        # Add all routes to the routes dictionary
        for i in jsonout['routes']:
            if i['route_name'] not in self.routes:
                self.routes[i['route_name']] = {
                    "route_type"    : i['route_type'],
                    "route_id"      : i['route_id'],
                    "route_gtfs_id" : i['route_gtfs_id'],
                    "Status"        : "",
                    "Status_Long"   : ""
                }

    def getallstatus(self):
        for route in self.routes:
            self.routes[route]["Status"],self.routes[route]["Status_Long"] = self.getdisruptions(self.routes[route]["route_id"])
            print("Updating {} status".format(route))

    def getdisruptions(self, route):
        r = requests.get(self.getsigurl(self.selecturl('checkline', route)))
        jsonout = r.json()
        # Filter down to train level
        parsedict = jsonout['disruptions']['metro_train']
        if bool(parsedict) == False:
            short, long = "Good service", "No planned outages"

        for subdict in parsedict:
            if subdict['display_on_board'] == False:
                short = 'Good service'
                long = 'Upcoming planned outages'
            else:
                short = "Delays"
                long = subdict['title']
        
        return short, long


    def selecturl(self, reqtype, route_id=0):
        apibase = '/v3/'

        if reqtype.lower() == 'refresh':
            apiurl = apibase + 'routes?route_types=0'
        elif reqtype.lower() == 'checkall':
            apiurl = apibase + 'disruptions?disruption_modes=1'
        elif reqtype.lower() == 'checkline':
            apiurl = apibase + 'disruptions/route/{}'.format(route_id)

        return apiurl

    
    def checkage(self):
        """
        Check if the age of our data is > 15 minutes
        Return:
        True - Less than 15 minutes old
        False - More than 15 minutes old
        """
        if self.age < datetime.datetime.now() - datetime.timedelta(minutes = 10):
            return True
        else:
            return False