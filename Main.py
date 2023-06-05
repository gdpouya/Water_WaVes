import threading
import time
import sys

# Define constants
cities=[]
timer=0
cities_name=["BARCELONA","MARSEILLE","GENOA","NAPLES","MESSINA"]

class Central_control():
    def __init__(self):
        # Initialize a semaphore to control access to shared resources
        self.control_semaphore = threading.Semaphore(1)
        
        # Set a flag indicating that the program has not ended yet
        self.end_program = True
        
    def request_sent(self, ship):
        # Acquire the semaphore to control access to shared resources
        self.control_semaphore.acquire()
        
        # Get the city where the ship is headed next
        dis_city = cities[ship.get_dis()]
        
        # Check if there is enough space available at the destination city to store the packages on the ship
        if dis_city.boat_num() > 0:
            # If there is enough space, grant permission for the ship to sail to its next destination
            print("Permission granted for Ship " + ship.get_ship_id() + " to sail, Time: " + str(timer))
            ship.go()
        
        # Release the semaphore to allow other threads to access shared resources
        self.control_semaphore.release()
        
    def start(self):
        # Read input from a file and start each city in the simulation
        with open('.\\Water_Waves\\input.txt', 'r') as f:
            txt = f.readline().split(' ')
            package_number = int(txt[2])
            
            for i in range(4):
                txt = f.readline().split(' ')
                city = City(i, int(txt[2]), int(txt[7]))
                cities.append(city)
                
            cities.append(City(4, 1, 0))
            cities[0].add_box(package_number)
        
        for city in cities:
            city.start()
            
    def check_end(self):
        # Check if all the required packages have been transported to their destinations
        if self.end_program:
            self.end_program = False
            
            for i in range(0, 4):
                self.end_program = self.end_program or not cities[i].end()
        else:
            print("end the program")
            sys.exit()

cc=Central_control()

class Ship(threading.Thread):
    def __init__(self, city, city_num, id, minimum):
        super().__init__()
        
        # Initialize a semaphore to control access to shared resources
        self.operator_semaphore = threading.Semaphore(1)
        
        # Set the status of the ship to not moving
        self.moving = False
        
        # Set the unique identifier of the ship
        self.ship_id = cities_name[city_num] + '_' + str(id)
        
        # Set the minimum number of packages that must be shipped on the ship
        self.minimum = minimum
        
        # Set the home city of the ship
        self.city_num = city_num
        self.city = city
        
        # Initialize a semaphore to signal when the ship is working
        self.working = threading.Semaphore(0)
        
        # Set the flag indicating whether the ship is idle or not
        self.work = True
        
    def run(self):
        # Run an infinite loop in which the ship waits until it has enough packages to make a trip
        while True:
            if self.city_num < 4 and self.city.boat_fill():
                # If there are enough packages, ask permission from the central control object to sail to its next destination
                print(str(self.ship_id) + " is home and asking for permission from " + cities_name[self.city_num] + " to " + cities_name[self.city_num + 1] + ", Time: " + str(timer))
                cc.request_sent(self)
                
            else:
                # If there are not enough packages, set the ship's work flag to false
                self.work = False
                
                # Check if all the required packages have been transported to their destinations
                cc.check_end()
                
                # Wait for another package to arrive
                self.working.acquire()
            
    def go(self):
        # Update the status of the ship to moving
        self.moving = True
        
        # Sail to the next city
        print(str(self.ship_id) + " is sailing with " + str(self.minimum) + " packages to " + cities_name[self.city_num + 1] + ", Time: " + str(timer))
        cities[self.city_num].boat(-1)
        time.sleep(5)
        cities[self.city_num + 1].add_box(self.minimum)
        time.sleep(3)
        cities[self.city_num].boat(1)
        
        # Update the status of the ship to not moving
        self.moving = False
        
    def is_moving(self):
        # Return whether the ship is currently moving or not
        return self.moving
    
    def get_dis(self):
        # Return the number of the city where the ship is headed next
        return self.city_num + 1
    
    def get_ship_id(self):
        # Return the unique identifier of the ship
        return self.ship_id
    
    def is_working(self):
        # Return whether the ship is idle or not
        return self.work
    
    def s(self):
        # Set the work flag to true and release the semaphore to signal that the ship is working
        self.work = True
        self.working.release()


class City(threading.Thread):
    def __init__(self, city, ship_number, storage):
        super().__init__()
        
        # Set the name of the city
        self.name = cities_name[city]
        
        # Set the number of ships stationed at the city
        self.boat_num_ = ship_number
        
        # Set the storage capacity of the city
        self.storage_ = storage
        
        # Initialize a list to hold the ships currently stationed at the city
        self.boats_ = []
        
        # Initialize a semaphore to control access to shared resources
        self.mutex_ = threading.Semaphore(1)
        
        # Initialize a semaphore to signal when packages arrive at the city
        self.packages = threading.Semaphore(0)
        
    def start(self):
        # Start each ship stationed at the city
        for i in range(self.boat_num_):
            boat = Ship(self, city, i, 5)
            self.boats_.append(boat)
            boat.start()
            
    def do_it_again(self):
        # Check if all the required packages have been transported to their destinations
        cc.check_end()
        
        # Wake up any ships that are idle and send them out again
        for boat in self.boats_:
            if not boat.is_working():
                print(str(boat.get_ship_id()) + " is back to work in " + self.name + ", Time: " + str(timer))
                boat.s()
                
    def end(self):
        # Return whether all the required packages have been transported to their destinations or not
        return self.storage_ == 0
    
    def print_data(self):
        # Print the name of the city
        print("City:", self.name)
    
    def boat_num(self):
        # Return the number of boats currently in the city
        return self.boat_num_
    
    def add_box(self, amount):
        # Add a new package to the city's storage capacity and wake up any waiting ships that are ready to sail
        self.mutex_.acquire()
        self.storage_ += amount
        self.mutex_.release()
        
        print(str(amount) + " packages arrived in " + self.name + ", Time: " + str(timer))
        self.packages.release()
        
    def boat_fill(self):
        # Check if a ship can sail from the city based on whether it has enough packages to fill the ship or not
        self.mutex_.acquire()
        if self.storage_ >= 5:
            self.storage_ -= 5
            self.mutex_.release()
            return True
        else:
            self.mutex_.release()
            return False
        
    def boat(self, i):
        # Update the number of boats currently in the city
        self.boat_num_ += i
        
    def joins(self):
        # Wait for all the ships in the city to finish their current trips before ending the program
        for boat in self.boats_:
            boat.join()
            
    def get_name(self):
        # Return the name of the city
        return self.name

if __name__ == '__main__':
    cc.start()