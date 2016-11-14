# proj8-Gcal
AUTHOR: Brian Leeson, bel@cs.uoregon.edu  
Skeleton code created by instructor: Michael Young  

## What is here
A simple webpage that finds potentially busy and free times in a specific date and time range. <br>

## Installation and running
Project only runnable with client_secrets.py, admin_secrets.py, and client_secret.json not included in the repo.

The user must have pyenv installed:  
sudo apt-get update  
sudo apt-get upgrade    
sudo apt-get install python3-venv  

git clone <URL> 
cd to the cloned repository  
make configure  
make run  

The default port is 5000. If your are on your own machine connect at localhost:5000.
If the server is running another machine connect at ipAddress:5000.

## Testing the application

Test this server by following the RUNNING instructions and attempt to connect to the server.

To run automated tests:
make test
