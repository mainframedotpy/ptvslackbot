from hashlib import sha1
import hmac
import requests

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
        self.refreshlines()
        self.age = 
        
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

    def selecturl(self, reqtype):
        apibase = '/v3/'

        if reqtype.lower() == 'refresh':
            apiurl = apibase + 'routes?route_types=0'
        elif reqtype.lower() == 'checkall':
            apiurl = apibase + 'disruptions?disruption_modes=1'

        return apiurl