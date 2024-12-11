# cecs-327-assignment-8
 
## Instructions on running client, server, and database:
1. For the server, make sure that you have the following libraries installed on your machine:
    - PyMongo (Needed for database access)
    - pytz (Needed for Timestamp conversions)
	- certifi (Need for database certificate verification)
    - If you don't have these libraries install, simply run the commands
		- "pip install pymongo" 
		- "pip install pytz"
		- "pip install certifi"

2. Run the server by navigating to the folder where server.py is in command prompt and running "py server.py"
    - Specify the port you'd want to communicate over, 22 is easiest as it is already open

3. Run the client by navigating to the folder where client.py is in command prompt and running "py client.py"
    - Specify the ip address of the server machine
    - Specify the port the server machine opened

4. You'll now be prompted with a menu screen of queries to make. Enter in the number of your choice
    1. Average moisture in the fridge (in past 3 hours)"
    2. Average water consumption per washing cycle in smart dishwasher"
    3. Device with the highest electricity consumption (fridge 1, fridge 2, dishwasher)"
    4. Exit

5. Wait for the response back from the server

6. Continue making requests, when you're done, type "exit" to quit, the server and client will then close.