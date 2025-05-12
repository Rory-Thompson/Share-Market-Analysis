import os
import sys
from config import aest  # Import the global timezone variable
from pytz import timezone
aest = timezone('Australia/Sydney')
from Dashboard_testing.Dashboard import Dashboard_creator

location_base = os.getenv("LOCATION", os.path.join(os.sep, "DiskStation","Data", "trading","files"))

#note have to pass the location variable if on linux. 
def main():
    if len(sys.argv) <2:
        api_location = "http://localhost:8080"
    else:
        api_location = sys.argv[1]

    location = os.path.join(location_base, "asx")#does automatic join
    location_model_res = os.path.join(location_base, "rory_model_results")#not used for now .
    print("main.py is runninng")
    
    app = Dashboard_creator(api_location = api_location, metric_location = location_base)
    app.run()

if __name__ == "__main__":
    main()