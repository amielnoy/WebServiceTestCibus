# Web Services Test Cibus

The solution is implemented based on flask python web framework
using local sqlite3 database

to be able to run the web services:  
1)open the project in PyCharm community edition
  define virtual env
  choose python 3.10 and above

2)Run the Server.
There are two options,

a)Run Python Script
From root folder of the project on cli(windows):
python app.py

b)using docker commands:
From root folder of the project on cli(windows):
run runDocker.bat

To run and test the various web services:

use the folowing postman collection,
import to postman the postman requests collection
WebServiceCibus.postman_collection.json

To run the unit tests:

from the project root
cd unit_testing
pytest web_services_tests.py
