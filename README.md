# ASX Automated Share Analyser/Visualiser

**what does this project aim to achieve?**
This project aims to automatically analyse all shares listed on the asx stock exchange and list a certain amount to buy for a given time. There are over 2500 shares it analyses, using at the moment fairly rudimentary techniques like RSI, rolling average cross, gradient averages. 

![Dashboard Preview](https://raw.githubusercontent.com/Rory-Thompson/Share-Market-Analysis/main/assets/dashboard_example.png)

This cannot be replicated on other networks as it uses local file locations in which all share data is stored. 

## How to load? 
- place a copy of the dockerfile somewhere on your machine you wish to host this website.
- run the following docker command: docker build --no-cache -t share_market_app .
- docker run -d -p 8050:8050 --name share_market_container -v *inser diskstationlocation* -e LOCATION=*inser diskstationlocation*/trading/files share_market_app
- the above command will run src/main.py on port 8050 of the desired machine. 
- log into machines local ip: 8050 port. Dashboard will load. 

## Usage:
The button update cache gets new data and loads it into cache then peforms analysis recomending new shares to purchase

**DO NOT CLICK THIS BUTTON ALOT**
_this button will take much time to load_

In order to save memory The first line graph only allows 2 shares. It is not much use with more anyway. 

Whenever new shares get loaded into buy, they will remain on the dashboard forever. And can be selected.

Any share that has been reccomended to purchase will remain in the data table and as options for the different graphs.

Appears to require about 600 MB of RAM which is not the best. All data  is loaded into cache at the moment. 
