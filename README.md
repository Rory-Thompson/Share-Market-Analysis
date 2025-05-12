# ASX Automated Share Analyser/Visualiser

**what does this project aim to achieve?**
This project aims to automatically analyse all shares listed on the asx stock exchange and list a certain amount to buy for a given time. There are over 2500 shares it analyses, using at the moment fairly rudimentary techniques like RSI, rolling average cross, gradient averages. 

![Dashboard Preview](https://raw.githubusercontent.com/Rory-Thompson/Share-Market-Analysis/main/assets/dashboard_example.PNG)

This cannot be replicated on other networks as it uses local file locations in which all share data is stored. 

## How to load? 
- place a copy of the dockerfile somewhere on your machine you wish to host this website.
- run the following docker command: docker build --no-cache -t share_market_app .
- docker run -d -p 8050:8050 --name share_market_container -v *inser diskstationlocation* -e LOCATION=*inser diskstationlocation*/trading/files share_market_app
- the above command will run src/main.py on port 8050 of the desired machine. 
- log into machines local ip: 8050 port. Dashboard will load. 
- in the python run command you must also pass an argument. the api location. if none is passed it will just do "http://localhost:8080"
