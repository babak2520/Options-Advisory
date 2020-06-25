
# Server
### Prerequisites
1. pip install -r requirements.txt

### Start the server
Go to the directory of server. Run flask at the port 8050 in command line (where client listens):
1. set FLASK_APP=server.py
2. set FLASK_ENV=development
3. flask run -h localhost -p 8050

# Client
### Prerequisites

1. Install [nodejs]([https://nodejs.org/en/download/](https://nodejs.org/en/download/))
2. Install vuejs cli globally:
	
		npm install -g @vue/cli


### Start the client
Go to the directory of the client. Run below commands in a separate command line. And in browser, go to the directory shown once the client starts.

1. npm install
2. npm run serve

# Notes

Everytime a new Python package is installed. Include it in the requirements.txt.