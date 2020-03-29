# chipotle_scraping_demo

Reposted from https://blog.stetsonblake.com/posts/chipotle_web_scraping/
---
title: Scraping Chipotle Store Locations
author: "Stetson Blake"
date: "2020-03-27"
---

## Introduction 

Web scraping has loads of interesting use cases. From financial forecasting to lead-gen, web scraping has several creative uses that you might not think about at first glance. For example, a burrito shop opening a new location might want to place their location further away from a Chipotle. What if you had a map of every Chipotle in the US? Would this help your burrito chain to analyze the market better? You bet. 


This quick tutorial will show you how to inspect almost any store location app, find an API back-end, retrieve data from it and save it to a well-formatted CSV. 

## Prerequisites

You'll need:

- [a local code editor](https://code.visualstudio.com/) 

- [Python 3 installed](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3) 

- The [requests library](https://requests.readthedocs.io/en/master/) for python

- [Postman](https://www.postman.com/) for Modifying HTTP Requests


## Step 1 - Inspecting the Store Map App

Open a web-browser and go to any store locator app. You can google <Store Name> Locations. Try to find a web-app that has an interactive map.  

We'll use [Chipotle's store locator](https://chipotle.com/order#menu)

Open up Chrome's Network tool in DevTools:

`Right Click in the page > Inspect > Network`

DevTools allows us to inspect the network requests that our browser makes to Chipotle's web servers.

Now, we'll tinker a bit with the page and see if we can't find the HTTP call that returns store locations. We'll use the page as normal and input a location and load it in the browser. 

Under the name column, you'll see the assets being requested from the server. 

To make our search a bit easier, we can click the XHR option and filter the requests down further. XHR is short for XMLHttpRequest, an API available to browser languages like Javascript to send and receive HTTP/S requests.  Ajax ( or Asynchronous Javascript and XML) requests are sometimes called an XHR request but these days we commonly see JSON, plaintext or HTML received back. 

Once you've filtered down the results, you can click through the results and view the response. In this case, we'll see a JSON response that looks very promising. We'll grab the response by clicking in the response box, using commad/control+a to select it all and command/control+c to save it to our clipboard. 

We'll paste the response into VS code and using the command Pallete, we can  Command+Shift+P and Type `Json Pretty Print` to format our data to be easier to read.

Looking through the JSON response, we see a key `data` that contains store location data. Some of the data included is latitude, longitude, realEstateCategory, and the public phone number!

## Step 2 - Getting ALL of the Data

Now that we have the correct request, we'll head back to Chrome DevTools to further tinker with the request. We have SOME Chipotle locations, but we'd like to have ALL of the Chipotle locations to do proper Burrito-Chain market analysis. 

On the same request we grabbed our JSON data from, we'll right-click it > Copy > Copy as cURL. 

Curl is a Linux utility commonly used for requesting data to or from a server. Chrome has a handy export option so we you replicate this same request in our terminal. 

Here is the copied request:


```
curl 'https://services.chipotle.com/restaurant/api/v2.1/search' -H 'Connection: keep-alive' -H 'Accept: application/json, text/plain, */*' -H 'Sec-Fetch-Dest: empty' -H 'Ocp-Apim-Subscription-Key: b4d9f36380184a3788857063bce25d6a' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' -H 'Chipotle-CorrelationId: OrderWeb-284f3eed-06a5-41fd-9a34-f64a8ccb8ca1' -H 'Content-Type: application/json' -H 'Origin: https://chipotle.com' -H 'Sec-Fetch-Site: same-site' -H 'Sec-Fetch-Mode: cors' -H 'Referer: https://chipotle.com/order' -H 'Accept-Language: en-US,en;q=0.9,la;q=0.8,pt;q=0.7' --data-binary '{"timestamp":"2020-3-29","latitude":36.169941199999975,"longitude":-115.1398296,"radius":80467,"restaurantStatuses":["OPEN","LAB"],"conceptIds":["CMG"],"orderBy":"distance","orderByDescending":false,"pageSize":10,"pageIndex":0,"embeds":{"addressTypes":["MAIN"],"publicPhoneTypes":["MAIN PHONE"],"realHours":true,"directions":true,"catering":true,"onlineOrdering":true,"timezone":true,"marketing":true}}' --compressed
```

Go ahead and open up Postman. Postman is a GUI-based tool that allows us to modify our request more easily and save it for later. Hit File > New and select Request. Name it something useful (Chipotle_Locations)  and save it to a folder within Postman.

Then, click File > Import > Paste Raw Text. Here, we can paste our copied curl request from Chrome and click import. Postman will import our curl-formatted request and we can begin to modify it. Go ahead and click Send and observe the same JSON response body from earlier that is returned. 

We can click the Body Tab in Postman to view the JSON body that is being sent to Chipotle's servers. We'll see two interesting keys to modify: radius and pageSize. Radius is probably our distance in kilometers or miles to search and pageSize is the number of results returned. Change radius to something a bit higher -- 9999999 should work well. For pageSize, we'll use 5000. There are a few other parameters sent, but we'll just change these two. 


```json
{
    "timestamp": "2020-3-29",
    "latitude": 36.169941199999975,
    "longitude": -115.1398296,
    "radius": 9999999,
    "restaurantStatuses": [
        "OPEN",
        "LAB"
    ],
    "conceptIds": [
        "CMG"
    ],
    "orderBy": "distance",
    "orderByDescending": false,
    "pageSize": 5000,
    "pageIndex": 0,
    "embeds": {
        "addressTypes": [
            "MAIN"
        ],
        "publicPhoneTypes": [
            "MAIN PHONE"
        ],
        "realHours": true,
        "directions": true,
        "catering": true,
        "onlineOrdering": true,
        "timezone": true,
        "marketing": true
    }
}
```

Send the request again and you'll notice it takes a while to return a response. Postman shows nearly 6 seconds response time and 8.7 megabyte response. We want to be respectful of Chipotle's server resources, so it's a good idea to not run this query multiple times. Using pagination is usually a far better idea if you'll be running these types of requests many times. 

We can grab our response from Postman and copy it to VScode. Use command/control+f to make a quick search on a unique field per result like `addressLine1`. My find shows 2632 results. Perfect.

## Step 3 - Writing a script to dump the data to CSV

Now that we have all of the Chipotles (or damn near), we want to automate the retrieval and sorting of the data. 

Luckily, Postman makes that really easy too. To the right, near the Send request button, you'll see `Code`. Click `Code` and we can convert our modified request to a Python Script with the `Python - Requests` option on the left pane. 

Copy the code and paste it into your IDE and save it as `ChipotleScraper.py` or similar. 

Our code is thus:

```python
import requests

url = "https://services.chipotle.com/restaurant/api/v2.1/search"

payload = "{\n    \"timestamp\": \"2020-3-29\",\n    \"latitude\": 36.169941199999975,\n    \"longitude\": -115.1398296,\n    \"radius\": 9999999,\n    \"restaurantStatuses\": [\n        \"OPEN\",\n        \"LAB\"\n    ],\n    \"conceptIds\": [\n        \"CMG\"\n    ],\n    \"orderBy\": \"distance\",\n    \"orderByDescending\": false,\n    \"pageSize\": 5000,\n    \"pageIndex\": 0,\n    \"embeds\": {\n        \"addressTypes\": [\n            \"MAIN\"\n        ],\n        \"publicPhoneTypes\": [\n            \"MAIN PHONE\"\n        ],\n        \"realHours\": true,\n        \"directions\": true,\n        \"catering\": true,\n        \"onlineOrdering\": true,\n        \"timezone\": true,\n        \"marketing\": true\n    }\n}"
headers = {
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/plain, */*',
  'Sec-Fetch-Dest': 'empty',
  'Ocp-Apim-Subscription-Key': 'b4d9f36380184a3788857063bce25d6a',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
  'Chipotle-CorrelationId': 'OrderWeb-284f3eed-06a5-41fd-9a34-f64a8ccb8ca1',
  'Content-Type': 'application/json',
  'Origin': 'https://chipotle.com',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Referer': 'https://chipotle.com/order',
  'Accept-Language': 'en-US,en;q=0.9,la;q=0.8,pt;q=0.7'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
```

Now that we're making the request with python, we want to save it to CSV so we can import to Excel, Postgres, mySQL, or any other database.

at the top of the script, import the JSON and CSV libraries so we can handle the JSON response object and write to csv.
```python
import json
import csv
```

Below the print response line, we'll use the python `with` statement to to write to a file, `ChipotleLocations.csv`. 

```python
with open('ChipotleLocations.csv', mode='w') as CSVFile:
    writer = csv.writer(CSVFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow([
        "restaurantNumber",
        "restaurantName"
    ])
```

Inside the with statement, we'll define a writer object with a few parameters to define our delimiter as a comma. 

Then, we write the first row with the columns corresponding to the data from the JSON response object. 

Inside the with statement, add the following code:

```python
    for store in stores['data']:
        row = []
        store_id = store["restaurantNumber"]
        store_name = store["restaurantName"]

        row.append(store_id)
        row.append(store_name)
        writer.writerow(row)
```

Here, we use a for loop to iterate over the objects inside of the data key of the JSON object. The script says: 

For each item (called `store`) inside of `stores['data']`:
- Create an empty `row` variable of type list `[]`
- Create a variable `store_id` that contains the current item in the iteration's `restaurantNumber`
- Create a variable `store_name` that contains the current item in the iteration's `store_name`
- Append or add the `store_id` variable to the list `row` defined above
- Append or add the `store_name` variable to the list `row`
- Use the CSV writer object to write `row` to the file `Chipotle_Locations.csv`
- Go to the next item in the iteration, until we reach the last item


Let's run the script with:

```bash
➜  chipotle_scraping_demo# python ChipotleScraper.py
```

After a few seconds, take a look in the same folder and you'll see a CSV output with the data!

Adding additional columns is as simple as pulling them from the JSON response object and adding the CSV column names. A few are nested deeper, so you'll have to use additional brackets `[]` to index and slice them. 
For example, latitude and longitude would look like:

```python
latitude = latitudelatitude = store["addresses"][0]["latitude"]
longitude = store["addresses"][0]["longitude"]
```

You can grab the full-script at 

## Conclusion

Congratulations! At this point you have a working web scraping script in Python. You've learned how to inspect network requests with Chrome's DevTools and modify requests in Postman. You're well equipped to begin scraping data with the requests library and chopping your data via Python.

If you enjoyed this post, consider joining our community for Web Scraping Developers -- [Scraping in Prod](https://scrapinginprod.com). I've also made a YouTube video covering this same post [here](https://www.youtube.com/watch?v=ZFoQleFUH9Y). 