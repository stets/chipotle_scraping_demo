import requests
import csv
import json

url = "https://services.chipotle.com/restaurant/api/v2.1/search"

payload = "{\n    \"timestamp\": \"2020-3-14\",\n    \"latitude\": 39.1031182,\n    \"longitude\": -84.5120196,\n    \"radius\": 8000467,\n    \"restaurantStatuses\": [\n        \"OPEN\",\n        \"LAB\"\n    ],\n    \"conceptIds\": [\n        \"CMG\"\n    ],\n    \"orderBy\": \"distance\",\n    \"orderByDescending\": false,\n    \"pageSize\": 5000,\n    \"pageIndex\": 0,\n    \"embeds\": {\n        \"addressTypes\": [\n            \"MAIN\"\n        ],\n        \"publicPhoneTypes\": [\n            \"MAIN PHONE\"\n        ],\n        \"realHours\": true,\n        \"directions\": true,\n        \"catering\": true,\n        \"onlineOrdering\": true,\n        \"timezone\": true,\n        \"marketing\": true\n    }\n}"

headers = {
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/plain, */*',
  'Sec-Fetch-Dest': 'empty',
  'Ocp-Apim-Subscription-Key': 'b4d9f36380184a3788857063bce25d6a',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
  'Chipotle-CorrelationId': 'OrderWeb-a2bb933d-f645-4f5b-931d-603c9aa006fc',
  'Content-Type': 'application/json',
  'Origin': 'https://www.chipotle.com',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Referer': 'https://www.chipotle.com/',
  'Accept-Language': 'en-US,en;q=0.9,la;q=0.8,pt;q=0.7'
}

response = requests.request("POST", url, headers=headers, data = payload)
stores = json.loads(response.text)

with open('ChipotleLocations.csv', mode='w') as CSVFile:
    writer = csv.writer(CSVFile, delimiter=",")

    writer.writerow([
        "restaurantNumber",
        "restaurantName", 
        "latitude", 
        "longitude"
    ])

    for store in stores['data']:
        row = []
        store_id = store["restaurantNumber"]
        store_name = store["restaurantName"]
        latitude = store["addresses"][0]["latitude"]
        longitude = store["addresses"][0]["longitude"]
        

        row.append(store_id)
        row.append(store_name)
        row.append(latitude)
        row.append(longitude)
        
        writer.writerow(row)