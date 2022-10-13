#Need to install requests package for python
#easy_install requests
import requests
import json

# Set the request parameters
url = [YOUR SNOW URL]

# Eg. User name="admin", Password="admin" for this code sample.
user = [YOUR SNOW USER]
pwd = [YOUR SNOW PASSWORD]

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

hivegeturl = [YOUR HIVE GET URL]

hiveheaders = {
    "Accept": "application/json",
    "api_key": [YOUR HIVE API KEY]
}


# Do the HTTP request
def lambda_handler(event, context):
    response = requests.get(url, auth=(user, pwd), headers=headers )
    
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    
    # Decode the JSON response into a dictionary and use the data
    snowCases = []
    hiveCaseNumber = []
    hivegetresponse = requests.get(hivegeturl, headers=hiveheaders)
    hivedata = hivegetresponse.json()
    for x in hivedata:
        customFields = x['customFields']
        for j in customFields:
            label = j['label']
            if label == 'ServiceNow Case Number':
                key = j['value']
                hiveCaseNumber.append(key)
    print(hiveCaseNumber)
    data = response.json()
    result = data['result']
    for i in result:
        caseNumber = i['number']
        title = i['short_description']
        description = i['description']
        account = i['account']
        sys_id = i['sys_id']
        titleString =  account+" - "+title
        print(titleString)
        # newTitle = json.loads(titleString)
        if caseNumber not in hiveCaseNumber:
            createurl = [YOUR HIVE CREATE URL]

            createpayload = {
                "customFields": [
                    {
                        "label": "ServiceNow Case Number",
                        "value": caseNumber
                    }
                ],
                "projectId": [YOUR PROJECT ID],
                "title": titleString,
                "description": description
            }
            createheaders = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "api_key": [YOUR HIVE API KEY]
            }
            
            createresponse = requests.post(createurl, json=createpayload, headers=createheaders)
            
            print(createresponse.text)

         