from tetpyclient import RestClient
import tetpyclient
import json
import requests.packages.urllib3
import sys
import os
import argparse
import time
import csv

from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime

from tetpyclient import RestClient
from tqdm import tqdm as progress
import urllib3

CEND = "\33[0m"     #End
CGREEN = "\33[32m"  #Information
CYELLOW = "\33[33m" #Request Input
CRED = "\33[31m"    #Error
URED = "\33[4;31m" 
Cyan = "\33[0;36m"  #Return

# =================================================================================
# See reason below -- why verify=False param is used
# python3 fileHashUpload.py --url https://192.168.30.4 --credential dmz_api_credentials.json
# feedback: Le Anh Duc - anhdle@cisco.com
# =================================================================================
requests.packages.urllib3.disable_warnings()


parser = argparse.ArgumentParser(description='Tetration Create App under scope')
parser.add_argument('--url', help='Tetration URL', required=True)
parser.add_argument('--credential', help='Path to Tetration json credential file', required=True)
args = parser.parse_args()


def CreateRestClient():
    """create REST API connection to Tetration cluster
    Returns:
        REST Client
    """
    rc = RestClient(args.url,
                    credentials_file=args.credential, verify=False)
    return rc

def GetVRFs(rc):
	resp = rc.get('/vrfs')

	if resp.status_code != 200:
		print("Failed to retrieve app scopes")
		print(resp.status_code)
		print(resp.text)
	else:
		return resp.json()

def GetRootScope(vrfs):
	rootScopes = []
	for vrf in vrfs:
		rootScopes.append([vrf["name"] , vrf["vrf_id"]])
	return rootScopes

def uploadHash(rc):
	#Upload whitelist or blacklist hash to Tetration root Scope. Sample csv: HashType,FileHash,FileName,Notes (SHA‐1,1AF17E73721DBE0C40011B82ED4BB1A7DBE3CE29,application_1.exe,Sample Notes)
	vrfs = GetVRFs(rc)
	RootScopesList = GetRootScope(vrfs)
	print (Cyan + "\nHere are the names and VRF ID of all the root scopes in your cluster: ")
	print(*RootScopesList, sep="\n")
	root_scope_name = input(CGREEN +"\nWhat is the root scope you want to upload filehash: ")
	b_w_List = input(CGREEN +"\nIs it blacklist or whitelist: ")
	file_path = "sampleFileHashUpload.csv"
	resp = rc.upload(file_path, "/assets/user_filehash/upload/" + root_scope_name + "/" + b_w_List)
	if resp.status_code == 200:
		print("\nUploaded sucessful!" + CEND)
	else:
		print("Error occured during upload hash")
		print("Error code: "+str(resp.status_code))
		sys.exit(3)

def main():
	rc = CreateRestClient()
	uploadHash(rc)

if __name__ == "__main__":
	main()