#This script scrapes data from NSE-India's Live Market Top Ten Gainers and Losers web page and creates html page with a table containing the details

import urllib.request
import json
import webbrowser

#Parse json data from the URL
def parse_URL(url):
	req = urllib.request.Request(url, headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip,deflate,sdch", "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36"})
	response = urllib.request.urlopen(req)
	# In Python 3, binary data, such as the raw response of a http request, is stored in bytes objects. 
	# json.loads() expects strings. 
	# The solution is to decode the bytes data to string data with the appropriate encoding, which you can find in the header.
	parsed_json = json.loads(response.read().decode('utf-8'))
	data = parsed_json['data']
	return data

#Create a html table with the parsed data
def create_table(data):
	table = "<table class='table table-striped table-hover'>"
	table += "<tr>"
	table += "<th>Symbol</th>"
	table += "<th>Open Price</th>"
	table += "<th>High Price</th>"
	table += "<th>Latest Ex Date</th>"
	table += "</tr>"
	for i in range(0, len(data)):
		table += "<tr>"
		table += "<td>" + data[i]["symbol"] + "</td>"
		table += "<td>" + data[i]["openPrice"] + "</td>"
		table += "<td>" + data[i]["highPrice"] + "</td>"
		table += "<td>" + data[i]["lastCorpAnnouncementDate"] + "</td>"
		table += "</tr>"
	table += "</table>"
	return table

#Create a html page containing the table data for gainers and losers
def write_html(data):
	html_str = """<html>
		     <head>
		     <title>NSE Top Ten Gainers and Losers</title>
		     <link rel='stylesheet' href='http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css' />
		     <script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.js'></script>
		     <script type='text/javascript' src='http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'></script>
		     </head>
		     <body> 
		     <ul class='nav nav-tabs'>
		     <li class='active'><a href='#gainers' data-toggle='tab'>Gainers</a></li>
		     <li><a href='#losers' data-toggle='tab'>Losers</a></li>
		     </ul>
		     <div class='tab-content'>
		     <div class='tab-pane active' id='gainers'>
		     {gainersData}
		     </div>
		     <div class='tab-pane' id='losers'>
		     {losersData}
		     </div>
		     </div> 
		     </body>
		     </html>""".format(gainersData = create_table(data['gainers']), losersData = create_table(data['losers']))
	return html_str

#The NSE website retrieves data from these JSON file urls.
topGainersUrl = "http://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"
topLosersUrl = "http://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json"
data = {} 
data['gainers'] = parse_URL(topGainersUrl)
data['losers'] = parse_URL(topLosersUrl)

html_file = open("NSETopGainersLosers.html", "w")
html_file.write(write_html(data))
html_file.close()
webbrowser.open_new_tab('NSETopGainersLosers.html')
