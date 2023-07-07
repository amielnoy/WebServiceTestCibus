# Web Services Test Cibus

The solution is implemented based on flask python web framework
using local sqlite3 database

## To run the web services:

## 1)Open the project in PyCharm community edition
  define virtual env
  choose python 3.10 and above

## 2)Run the Server.

There are two options,

1. ###   Run Python Script
    From root folder of the project on cli(windows):
    
`  python app.py`
  
2. ###   Using docker commands:

    From root folder of the project on terminal(windows):
    
    `runDocker.bat`

# **To run and test the various web services:**

use the folowing postman collection,
import to postman the postman requests collection
WebServiceCibus.postman_collection.json
located at the root of the project
# **To run the unit tests:**

from the project root
**Run on terminal:**

`pytest unit_testing/web_services_tests.py`
