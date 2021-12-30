from py2cytoscape import cyrest
from requests.exceptions import ConnectionError
import time
import sys
import sys
import requests
import urllib.request as urllib2		
import json
from json import JSONDecodeError
import subprocess

from requests.models import Response


##########################################################################################################
##########################################################################################################
'''
The following functions are a unique implementation for handling Cytoscape 
requests and responses

based off:
    py2cytoscape.cyrest
    py2cytoscape.base

'''

HOST = 'localhost'
IP=HOST # temporary
PORT = 1234
VERSION = 'v1'
BASE_URL = 'http://' + HOST + ':' + str(PORT) + '/' + VERSION + '/'
HEADERS = {'Content-Type': 'application/json'}
VERBOSE=False

def checkresponse(r,verbose=False):
    status=r.status_code
    if 200 <= status < 300:
        if verbose:
            print("response status "+status)
            sys.stdout.flush()
        res=None
    else:
        print(r, r.status_code)
        sys.stdout.flush()
        res="error::"+str(r.status_code)
    return res

def handle_status_codes(x,verbose=False):
    if type(x) == str:
        if "error::" in x:
            res=int(x.lstrip("error::"))
        else:
            res=None
    else:
        res=None

    if res or verbose:
        if res:
            res=res
        else:
            res=x
    else:
        res=None

    if not res:
        if x:
            res=x

    return res


def api(namespace=None, command="", PARAMS={}, 
        body=None, host=HOST, port=str(PORT), 
        version=VERSION, method="POST", verbose=VERBOSE, 
        url=None, parse_params=True):
    """
    General function for interacting with Cytoscape API.

    :param namespace: namespace where the request should be executed. eg. "string"
    :param commnand: command to execute. eg. "protein query"
    :param PARAMs: a dictionary with the parameters. Check your swagger normaly running on
    http://localhost:1234/v1/swaggerUI/swagger-ui/index.html?url=http://localhost:1234/v1/commands/swagger.json
    :param host: cytoscape host address, default=cytoscape_host
    :param port: cytoscape port, default=1234
    :param version: API version
    :param method: type of http call, ie. "POST" or "GET" or "HELP".
    :param verbose: print more information

    :returns: For "POST" the data in the content's response. For "GET" None.

    eg.
    cytoscape("string","pubmed query",{"pubmed":"p53 p21","limit":"50"})
    """

    if url:
        baseurl=url
    else:
        if namespace:
            baseurl="http://"+str(host)+":"+str(port)+"/"+str(version)+"/commands/"+str(namespace)+"/"+str(command)
        else:
            baseurl="http://"+str(host)+":"+str(port)+"/"+str(version)+"/commands"

    if (method == "GET") or (method == "G"):
        URL=baseurl
        if verbose:
            print("'"+URL+"'")
            sys.stdout.flush()
        r = requests.get(url = URL, params=PARAMS)
        verbose_=checkresponse(r, verbose=verbose)
        if (verbose) or (verbose_):
            print("'"+URL+"'")
            sys.stdout.flush()

        if verbose_:
            res=verbose_
        else:
            res=r

    if (method == "DELETE"):
        URL=baseurl
        if verbose:
            print("'"+URL+"'")
            sys.stdout.flush()
        r = requests.delete(url = URL)
        verbose_=checkresponse(r, verbose=verbose)
        if (verbose) or (verbose_):
            print("'"+URL+"'")
            sys.stdout.flush()
        res=r.json()
        if len(res["errors"]) > 0:
            raise ValueError(res["errors"][0])

    elif (method == "POST") or (method == "P"):
        if verbose:
            print("'"+baseurl+"'")
            sys.stdout.flush()
        r = requests.post(url = baseurl, json = PARAMS)
        verbose_=checkresponse(r, verbose=verbose)
        if (verbose) or (verbose_):
            verbose=True
            print(r.content)
            sys.stdout.flush()

        res=r.json()
        if "errors" in res.keys():
            if len(res["errors"]) > 0:
                raise ValueError(res["errors"][0])
        if not verbose:
            if "data" in res.keys():
                res=res["data"]
        else:
            res=verbose_

    elif (method == "PUT"):
        if verbose:
            print("'"+baseurl+"'")
            sys.stdout.flush()
        r = requests.put(url = baseurl, json = body)

        verbose_=checkresponse(r, verbose=verbose)
        if (verbose) or (verbose_):
            verbose=True
            print(r.content)
            sys.stdout.flush()

        try:
            res=r.json()
            if "errors" in res.keys():
                if len(res["errors"]) > 0:
                    raise ValueError(res["errors"][0])
        except JSONDecodeError:
            if not r.text:
                res = {}
            else:
                raise

    elif (method=="HTML") or (method == "H") or (method=="HELP"):
        URL = baseurl
        if verbose:
            print("'"+URL+"'")
            sys.stdout.flush()
        response = requests.get(URL, params=PARAMS)

        res = response.text.split("\n")
        def clean(x):
            r=x.split("</p>")[0].split(">")[-1]
            return r
        res="\n".join([ clean(x) for x in res ])

    res=handle_status_codes(res,verbose=verbose)

    return res

def _status(cyrest_client, host, port, verbose=False):
    """
    Checks the status of your CyREST server.
    """
    _url = 'http://' + host + ':' + str(port) + '/' + 'v1' + '/'
    try:
        response=api(url=_url, method="GET", verbose=verbose)
        print('CyREST online!')
        return response
    except Exception as e:
        print('Connecting to Cytoscape ...')

##########################################################################################################
##########################################################################################################
       

def check_cyrest(port):
    print('start supervisord client')
    try:
        
        subprocess.run([
            "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"
        ],
        check=True)
    except subprocess.CalledProcessError as e:
         print('an error has occurred while trying to run TPS\n\n' + str(e))

    connection = False
    while not connection:
        try:
            print(f"try port {port}")
            cytoscape = cyrest.cyclient(host='localhost', port=port)
            status = _status(cytoscape, 'localhost', port)
            if not isinstance(status, requests.models.Response):
                time.sleep(4)
            else:
                if status.ok and status.status_code == 200:
                    connection = True
                    print('connection successful, exiting script')
                else:
                    print(f"{status.status_code}")
                    sys.exit()
        except ConnectionError as e:
            print(e)
            sys.exit()


if __name__ == '__main__':
    check_cyrest(1234)