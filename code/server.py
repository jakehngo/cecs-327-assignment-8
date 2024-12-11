import socket
from pymongo import MongoClient

# const value for the size of the buffer for the program
BUFFERSIZE = 1024

# Retrieve the database, and return the collection where our data is stored
def get_database():
   connection_string = "mongodb+srv://dngojngo:passwordjake@cluster0.crczq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
   client = MongoClient(connection_string)

   return client["test"]["my database_virtual"]

# Gets average moisture within a specified duration
def get_average_moisture(db, duration):
   from datetime import datetime, timedelta
   import pytz

   fridge_board_name = "Raspberry Pi 4 - FridgeBoard"
   moisture_meter_name = "Moisture Meter - Fridge"

   #converts the current time to utc because our data is in utc
   time_limit = datetime.now(pytz.utc) - timedelta(hours=duration)

   fridge_data = db.find({
         "payload.board_name": fridge_board_name, 
         "time": {"$gte": time_limit}
       })

   moisture_levels = [float(entry["payload"][moisture_meter_name]) for entry in fridge_data]

   return sum(moisture_levels) / len(moisture_levels) if moisture_levels else 0

# Gets the average water consumption
def get_average_water_consumption(db):
   dishwaser_board_name = "Raspberry Pi 4 - Dishwasher"
   water_flow_sensor_name = "Water Flow Sensor"

   water_data = db.find({ "payload.board_name": dishwaser_board_name })
   water_consumption = [float(entry["payload"][water_flow_sensor_name]) for entry in water_data]
   return sum(water_consumption) / len(water_consumption) if water_consumption else 0

# Gets the total power consumption a device has
def get_total_power_consumption_for_device(db, board_name, ammeter_name):
   power_data = db.find({"payload.board_name": board_name})
   power_consumption = [float(entry["payload"][ammeter_name]) for entry in power_data]
   return sum(power_consumption) if power_consumption else 0

# Compares the three devices and returns the one that uses the highest energy
def get_highest_energy_device(db):
   dishwasher_power = get_total_power_consumption_for_device(db, "Raspberry Pi 4 - Dishwasher", "Ammeter-Dishwasher")
   fridge_one_power = get_total_power_consumption_for_device(db, "Raspberry Pi 4 - FridgeBoard", "Ammeter" )
   fridge_two_power = get_total_power_consumption_for_device(db, "board 1 6ae5d072-105b-4c1f-9263-fc7bb6a6d940", "sensor 1 6ae5d072-105b-4c1f-9263-fc7bb6a6d940" )

   max_power_device = max( ("dishwasher", dishwasher_power), ("fridge 1", fridge_one_power), ("fridge 1", fridge_two_power), key=lambda x: x[1])
   return max_power_device[0]

# Takes a query from the client and chooses how to process it
def handle_query(query, db):
   try:
        print("Processing query...")
        if query == "average_moisture":
            avg_moisture = get_average_moisture(db, 3)
            return f"Average moisture inside the fridge over the past 3 hours in RH%: {avg_moisture:.2f}%"

        elif query == "average_water_consumption":
            avg_water = get_average_water_consumption(db)
            return f"Average water consumption per cycle: {avg_water:.2f} gallons"

        elif query == "highest_energy_device":
            max_power_device = get_highest_energy_device(db)
            return f"The device with the highest electricity consumption is the {max_power_device}"

        else:
            return "Sorry, this query cannot be processed."

   except KeyError as e:
        return f"Invalid query structure or missing data: {e}"
   
# Handles the processing of a single client connection
def handle_client(client_socket, client_address, db):
   # wth handles closing and errors for client socket
        with client_socket:
            print(f"Connected to {client_address}")
            while True:
              # gets buffer data from the client
              data = client_socket.recv(BUFFERSIZE)
              # if there is nothing we failed and break
              if not data:
                 print(f"Connection with {client_address} closed.")
                 return
                    
              # decode the buffer and handle that received message
              query = data.decode()
              # comfirms that we receive the message
              print(f"Received query: {query}")
              response = handle_query(query, db)
              # send that uppercase response back to the client
              client_socket.sendall(response.encode())
              print("Query Proccessed.\n")


def main():
   db = get_database()

   # get the port number from the user
   port = int(input("Please enter a port number: "))
    
   # create a tcp socket
   # using the with makes it so that it takes care of closing and etc.
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
      # listen in the port provided by the user
      server_socket.bind(("", port))
      server_socket.listen(5) # allows for 5 connections
      # confirm that the server is listening on that port
      print(f"Server is listening...")

      # accepts a connection with a client
      client_socket, client_address = server_socket.accept()
      handle_client(client_socket, client_address, db)

      # Exits program
      print("Server finished handling the client. Exiting...")

         
if __name__ == "__main__":
 main()

