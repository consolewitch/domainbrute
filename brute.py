#!/usr/bin/python
'''
This script uses the following libraries:
    argparse - for handling command line arguments
    requests - for handling api requests
    xml.etree.ElementTree - for parsing the XML response
    sys - for writing to stdout with more grace than generally available from 'print'
    time - for pausing between each api request

author: terminal@ter.minal.pw

'''

import argparse, requests, xml.etree.ElementTree, sys, time
xml.etree.ElementTree.register_namespace('',"http://api.namecheap.com/xml.response")

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, prog='brute.py',description='check availability of a particular domain')
#parser.add_argument('domain', metavar='domain', type=str, help='domain name without tld')
parser.add_argument('dictionary', metavar='dictionary', type=str, help='file of dictionary words')
parser.add_argument('delay', metavar='delay', type=int, help='time to wait between each api request to avoid rate limiting',default=2)
parser.add_argument('tld', metavar='tld', type=str, help='top level domain to search in',default=".com")
args=parser.parse_args()


''' read config file '''


''' constants '''
serviceUrl=""
apiKey="" #read this from api.key file
apiUser=""
apiUserName="" #for some reason namecheap requires the name in two different vars
apiClientIp="" #This must be an IP that you have whitelisted in the namecheap API


''' generate next random option from pattern '''


''' implementation '''
def isAvailable(domainName):
    apiResult = requests.get(serviceUrl + "?" + "ApiUser=" + apiUser + "&" + "ApiKey=" + apiKey + "&" + "UserName=" + apiUserName + "&" + "Command=namecheap.domains.check" + "&" + "ClientIp=" + apiClientIp + "&" + "DomainList=" + domainName)
    apiResult.encoding = 'utf-8'
    apiResultXmlTree = xml.etree.ElementTree.XML(apiResult.text)
    ### todo : we need to be grabbing the xml namespace from the results rather than setting it manually as below
    apiResultXmlLimb = apiResultXmlTree.find(".//{http://api.namecheap.com/xml.response}DomainCheckResult")
    return apiResultXmlLimb.attrib.get("Available")  

with open(args.dictionary,'r') as dictionary:
    for line in dictionary:
        time.sleep(args.delay)
        if isAvailable(line.rstrip('\n') + args.tld) == "true":
            print "\n" + line.rstrip('\n') + args.tld + " is available"
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
