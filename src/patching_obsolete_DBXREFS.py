import requests, json, sys

HEADERS = {'accept': 'application/json'}
POST_HEADERS = {'accept': 'application/json', 'Content-Type': 'application/json'}

#SERVER = "https://test.encodedcc.org/"
SERVER = "https://www.encodeproject.org/"
DEBUG_ON = False

def getKeyPair(path_to_key_pair_file, server_name):
    keysf = open(path_to_key_pair_file, 'r')
    keys_json_string = keysf.read()
    keysf.close()
    keys = json.loads(keys_json_string)
    key_dict = keys[server_name]
    AUTHID = key_dict['key']
    AUTHPW = key_dict['secret']
    return (AUTHID, AUTHPW)


def get_ENCODE(obj_id):
	'''GET an ENCODE object as JSON and return as dict
	'''
	DEBUG_ON = False
	url = SERVER+obj_id+'?limit=all'
	#url = SERVER+obj_id
	if DEBUG_ON:
		print "DEBUG: GET %s" %(url)
	response = requests.get(url, auth=(AUTHID, AUTHPW), headers=HEADERS)
	if DEBUG_ON:
		print "DEBUG: GET RESPONSE code %s" %(response.status_code)
		try:
			if response.json():
				print "DEBUG: GET RESPONSE JSON"
				print json.dumps(response.json(), indent=4, separators=(',', ': '))
		except:
			print "DEBUG: GET RESPONSE text %s" %(response.text)
	if not response.status_code == requests.codes.ok:
		response.raise_for_status()
	return response.json()

def patch_ENCODE(obj_id, patch_input):
    '''PATCH an existing ENCODE object and return the response JSON
    '''
    if isinstance(patch_input, dict):
        json_payload = json.dumps(patch_input)
    elif isinstance(patch_input, basestring):
            json_payload = patch_input
    else:
            print >> sys.stderr, 'Datatype to patch is not string or dict.'
    url = SERVER+obj_id
    if DEBUG_ON:
            print "DEBUG: PATCH URL : %s" %(url)
            print "DEBUG: PATCH data: %s" %(json_payload)
    response = requests.patch(url, auth=(AUTHID, AUTHPW), data=json_payload, headers=POST_HEADERS)
    if DEBUG_ON:
            print "DEBUG: PATCH RESPONSE"
            print json.dumps(response.json(), indent=4, separators=(',', ': '))
    if not response.status_code == 200:
        print >> sys.stderr, response.text
    return response.json()




keypair = getKeyPair('keypairs.json', 'test')

AUTHID = keypair[0]
AUTHPW = keypair[1]

mone = 0
table_f = open('obsolete_list.list', 'r')
for l in table_f:
    # print (l)
    arr = l.strip().split()
    acc = arr[0]
    dbxrefs_to_update = arr[1:]
    print (acc + '\t' + str(dbxrefs_to_update))

    ex = get_ENCODE(acc)
    if 'dbxrefs' in ex:
        old_dbxrefs = ex['dbxrefs']
    else:
        old_dbxrefs = []
    new_dbxrefs = []
    for entry in old_dbxrefs:
        if entry not in dbxrefs_to_update:
            new_dbxrefs.append(entry)
        else:
            new_dbxrefs.append('GEO-obsolete' + entry[3:])
    print (new_dbxrefs)
    patch_input = {"dbxrefs": new_dbxrefs}    
    patch_ENCODE(acc, patch_input)
    #new_list = old_dbxrefs
    #print (new_list)

    #new_list.append('GEO:'+arr[0])
    #print (new_list)
    '''
    mone += 1
    arr = l.strip().split()

    print (str(mone) +'\t'+arr[1]+'\t'+arr[0])
    f = get_ENCODE(arr[1])
    #print f['dbxrefs']
    if 'dbxrefs' in f:
        old_dbxrefs = f['dbxrefs']
    else:
        old_dbxrefs = []
    new_list = old_dbxrefs
    #print (new_list)

    new_list.append('GEO:'+arr[0])
    #print (new_list)
    
    patch_input = {"dbxrefs": new_list}
    #print (patch_input)
    
    patch_ENCODE(arr[1], patch_input)
    '''

table_f.close()