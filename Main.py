import threading
import time
cities=[]
time=0
cities_name=["BARCELONA","MARSEILLE","GENOA","NAPLES","MESSINA"]

class Central_control():
    def __init__(self):
        self.control_semaphore=threading.Semaphore(1)
    def request_sent(self,ship):
        self.control_semaphore.acquire()
        dis_city=cities[ship.get_dis()]
        dis_city.print_data()
        if(dis_city.boat_num > 0):
            ship.go()
            print("Permission granted for Ship "+ship.get_ship_id+"to sail, Time: "+str(time))
        self.control_semaphore.release()
    def start(self):
        with open('.\\Water_Waves\\input.txt','r') as f:
            txt=f.readline().split(' ')
            package_number=int(txt[2])
            for i in range(4):
                txt=f.readline().split(' ')
                city=City(i,int(txt[2]),int(txt[7]))
                cities.append(city)
            cities.append(City(4,1,0))
            cities[0].add_box(package_number)
        end_program=True
        for city in cities:
            city.start()
            end_program=end_program and city.end()
        if(~end_program):
            self.start()

cc=Central_control()
class Ship(threading.Thread):
    def __init__(self,city,city_num,id,minimum):
        super().__init__()
        self.operator_semaphore = threading.Semaphore(1)
        self.moving = False
        self.ship_id=cities_name[city_num]+'_'+str(id)
        self.minimum=minimum
        self.city_num=city_num
        self.city=city
        self.boxes=0
    def run(self):
        if(self.city.boat_fill()):
            print(str(self.ship_id)+" is home and asking for permission from "+cities_name[self.city_num]+" to "+cities_name[self.city_num+1]+" , Time: "+str(time))
            cc.request_sent(self)
            
    def go(self):
        self.moving=True
        print(str(self.ship_id)+" is sailing with "+str(self.minimum)+" packages to "+cities_name[self.city_num+1]+" , Time: "+str(time))
        cities[self.city_num].boat(-1)
        time.sleep(5)
        cities[self.city_num+1].add_box(self.minimum)
        time.sleep(3)
        cities[self.city_num].boat(1)
        self.moving=False
    def is_moving(self):
        return self.moving
    def get_dis(self):
        return self.city_num+1
    def get_ship_id(self):
        return self.ship_id
        

class City():
    def __init__( self , city , ship_number , storage) :
        self.city_name=cities_name[city]
        self.ships = []
        self.ship_in_city=ship_number
        self.end_task=False
        self.storage=0
        self.ship_storage=storage
        self.change_storeage_sf=threading.Semaphore(1)
        self.boat_arrive=threading.Semaphore(1)
        self.boxes_check_semaphore = threading.Semaphore(1)
        for i in range (0,ship_number):
            self.ships.append(Ship(self,city,i,storage))
    def start(self):
        if(self.storage < self.ship_storage):
            self.end_task=True
        else:
            for ship in self.ships:
                ship.start()
    def end(self):
        return self.end_task
    def print_data(self):
        print(self.city_name)
    def boat_num(self):
        return self.ship_in_city
    def add_box(self,amount):
        self.end_task=False
        self.change_storeage_sf.acquire()
        self.storage += amount
        self.change_storeage_sf.release()
        for ship in self.ships:
            if(~ship.is_moving()):
                ship.start()
    def boat_fill(self):
        self.change_storeage_sf.acquire()
        if(self.storage > self.ship_storage):
            self.storage -= self.ship_storage
            if(self.storage<self.ship_storage):
                self.end_task=True
            self.change_storeage_sf.release()
            return True
        else:
            self.change_storeage_sf.release()
            return False
    def boat(self,i):
        self.boat_arrive.acquire()
        self.boat_num += i
        self.boat_arrive.release()
        

if __name__ == '__main__':
    cc.start()
    print("end the program Bye Bye")