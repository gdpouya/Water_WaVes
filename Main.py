import threading
import os
cities=[]
cities_name=["BARCELONA","MARSEILLE","GENOA","NAPLES","MESSINA"]
class Ship(threading.Thread):
    def __init__(self,city,city_num,id,minimum):
        super().__init__()
        self.operator_semaphore = threading.Semaphore(1)
        self.moving=True
        self.boxes_check_semaphore = threading.Semaphore(1)
        self.ship_id=cities_name[city_num]+'_'+str(id)
        self.minimum=minimum
        self.city_num=city_num
        self.city=city
        self.boxes=0
    def run(self):
        while(cities[self.city_num].storage < self.minimum):
            self.boxes_check_semaphore.acquire()
    
        
        

class City(threading.Thread):
    def __init__( self , city , ship_number , storage) :
        super().__init__()
        self.city_name=cities_name[city]
        self.ships = []
        self.ship_in_city=ship_number
        self.end_task=False
        self.storage=0
        self.ship_storage=storage
        self.change_storeage_sf=threading.Semaphore(1)
        # for i in range (0,ship_number):
        #     self.ships.append(Ship(self,city,i,storage))
    def run(self):
        print("hi")
        if(self.storage < self.ship_storage):
            self.end_task=True
        else:
            for ship in self.ships:
                ship.start()
    def end(self):
        return self.end_task
    def print_data(self):
        print(self.city_name)
        
class Central_control:
    def __init__(self):
        self.control_semaphore=threading.Semaphore(1)
    def request_sent(self,Ship):
        self.control_semaphore.acquire()
        
    def start(self):
        with open('.\\Water_Waves\\input.txt','r') as f:
            txt=f.readline().split(' ')
            package_number=int(txt[2])
            for i in range(4):
                txt=f.readline().split(' ')
                city=City(i,int(txt[2]),int(txt[7]))
                cities.append(city)
            cities.append(City(4,-1,0))
        end_program=True
        for city in cities:
            city.start()
            end_program=end_program and city.end()
        for city in cities:
            city.join()
        if(~end_program):
            self.start()

if __name__ == '__main__':
    # print(os.getcwd())
    
    cc=Central_control()
    cc.start()
    print("end the program Bye Bye")