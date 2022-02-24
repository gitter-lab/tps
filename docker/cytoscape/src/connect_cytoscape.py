'''
The following is derived from py2cytoscape.cyrest.base, 
https://github.com/cytoscape/py2cytoscape, which implements a RESTful API
client for Cytoscape available under the MIT License, Copyright (c) 2014-2015
University of California, San Diego Trey Ideker Lab

Citation:
    Ono, K. et al. (2015) CyREST: Turbocharging Cytoscape Access for External Tools via a RESTful API. F1000Res, 4, 478

'''
import argparse
from re import S
from tabnanny import verbose
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
import os

from py2cytoscape.data.cyrest_client import CyRestClient

from requests.models import Response


##########################################################################################################
##########################################################################################################
'''
The following functions are a unique implementation for handling Cytoscape 
requests and responses

based off:
    py2cytoscape.cyrest
    py2cytoscape.cyrest.base

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
       

# def check_cyrest(port):
#     print('start supervisord client')
#     try:
#         subprocess.run([
#             "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"
#         ],
#         check=True)
#     except subprocess.CalledProcessError as e:
#          print('an error has occurred while trying to run TPS\n\n' + str(e))

#     connection = False
#     while not connection:
#         try:
#             print(f"try port {port}")
#             cytoscape = cyrest.cyclient(host='localhost', port=port)
#             status = _status(cytoscape, 'localhost', port)
#             if not isinstance(status, requests.models.Response):
#                 time.sleep(4)
#             else:
#                 if status.ok and status.status_code == 200:
#                     connection = True
#                     print('connection successful, exiting script')
#                 else:
#                     print(f"{status.status_code}")
#                     sys.exit()
#         except ConnectionError as e:
#             print(e)
#             sys.exit()


def get_parser() -> argparse.ArgumentParser:
    '''
    :return: an argparse ArgumentParser object for parsing command
        line parameters
    '''
    parser = argparse.ArgumentParser(
        description='Run Cytoscape pipeline.')

    parser.add_argument('--save',
        help='cytoscape session file')
    parser.add_argument('--style', help='style file')
    parser.add_argument('--annot', help='annotations file')
    parser.add_argument('--network', help='network file')
    parser.add_argument('--datatypes', help='data types for columns')

    return parser

def parse_arguments():
    '''
    Initialize a parser and use it to parse the command line arguments
    :return: parsed dictionary of command line arguments
    '''
    parser = get_parser()
    opts = parser.parse_args()

    return opts

class CytoscapeClient:

    def __init__(self, save_file, style_file, annot_file, network_file, data_types) -> None:
        self.save_file = save_file
        self.style_file = style_file
        self.annot_file = annot_file
        self.network_file = network_file
        self.data_types = data_types

    def __visualize_outputs(self, cyclient):
        _annot_file = os.path.abspath(self.annot_file)
        _style_file = os.path.abspath(self.style_file)

        cy = CyRestClient()
        cy.session.delete()
        cy.network.create_from(self.network_file)
        time.sleep(2)
        style = cyclient.vizmap.load_file(_style_file)
        cyclient.vizmap.apply(style[0])
        cyclient.table.import_file(
            afile=_annot_file,
            firstRowAsColumnNames=True,
            keyColumnIndex='1',
            startLoadRow='0',
            delimitersForDataList='|',
            dataTypeList=self.data_types
        )
        session_full_file = os.path.abspath(self.save_file)
        cyclient.session.save_as(session_file=session_full_file)


    def check_cyrest(self, port):
        print('start supervisord client')
        try:
            subprocess.run([
                "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"
            ],
            check=True)
        except subprocess.CalledProcessError as e:
            print('an error has occurred while trying to run TPS\n\n' + str(e))

        connection = False
        attempts = 0

        print(f"try port {port}")
        while not connection:
            try:
                cytoscape = cyrest.cyclient(host='localhost', port=port)
                status = _status(cytoscape, 'localhost', port)
                if not isinstance(status, requests.models.Response):
                    time.sleep(4)
                    attempts+=1
                else:
                    if status.ok and status.status_code == 200:
                        connection = True
                        self.__visualize_outputs(cytoscape)
                        print('connection successful, exiting script')
                    else:
                        print(f"{status.status_code}")
                        sys.exit()
            except ConnectionError as e:
                print(e)
                sys.exit()

def main():
    opts = parse_arguments()
    style_file = opts.style
    save_file = opts.save
    annot_file = opts.annot
    network_file = opts.network
    data_types = opts.datatypes

    cyclient = CytoscapeClient(save_file, style_file, annot_file, network_file, data_types)
    cyclient.check_cyrest(1234)


if __name__ == '__main__':
    main()
