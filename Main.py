import threading
import time
import sys
cities=[]
timer=0
cities_name=["BARCELONA","MARSEILLE","GENOA","NAPLES","MESSINA"]

class Central_control():
    def __init__(self):
        self.control_semaphore=threading.Semaphore(1)
        self.end_program=True
    def request_sent(self,ship):
        self.control_semaphore.acquire()
        dis_city=cities[ship.get_dis()]
        if(dis_city.boat_num() > 0):
            print("Permission granted for Ship "+ship.get_ship_id()+" to sail, Time: "+str(timer))
            ship.go()
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
        for city in cities:
            city.start()
    def check_end(self):
        #print("try to end ")
        if(self.end_program):
            self.end_program=False
            for i in range(0,4):
                #print(str(cities[i].get_name())+" end is "+str(cities[i].end()))
                self.end_program=self.end_program or not cities[i].end()
        else:
            print("end the program")
            sys.exit()

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
        self.working=threading.Semaphore(0)
        self.work=True
    def run(self):
        while(True):
            if(self.city_num < 4 and self.city.boat_fill()):
                print(str(self.ship_id)+" is home and asking for permission from "+cities_name[self.city_num]+" to "+cities_name[self.city_num+1]+" , Time: "+str(timer))
                cc.request_sent(self)
            else:
                self.work=False
                #print(str(self.ship_id)+" is sleeped")
                cc.check_end()
                self.working.acquire()
            
    def go(self):
        self.moving=True
        print(str(self.ship_id)+" is sailing with "+str(self.minimum)+" packages to "+cities_name[self.city_num+1]+" , Time: "+str(timer))
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
    def is_working(self):
        return self.work
    def s(self):
        #print(str(self.ship_id)+" is waked up")
        self.work=True
        self.working.release()
        

class City():
    def __init__( self , city , ship_number , storage) :
        super().__init__()
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
        for ship in self.ships:
            ship.start()
            
    def do_it_again(self):
        if(self.storage < self.ship_storage):
                self.end_task=True
        else:
            for ship in self.ships:
                if(~ship.is_working()):
                    ship.s()
    def end(self):
        return self.end_task
    def print_data(self):
        print(self.city_name)
    def boat_num(self):
        return self.ship_in_city
    def add_box(self,amount):
        #print(str(self.city_name)+" storage have "+str(self.storage))
        self.end_task=False
        self.change_storeage_sf.acquire()
        self.storage += amount
        self.change_storeage_sf.release()
        for ship in self.ships:
            #print("try to wake "+str(ship.get_ship_id())+" up")
            #print(str(ship.get_ship_id())+" moving: "+str(ship.is_moving())+" working: "+str(ship.is_working()))
            if(not ship.is_moving() and not ship.is_working()):
                ship.s()
        #print(str(self.city_name)+" storage have "+str(self.storage))
    def boat_fill(self):
        self.change_storeage_sf.acquire()
        if(self.storage >= self.ship_storage):
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
        self.ship_in_city += i
        self.boat_arrive.release()
    def joins(self):
        for ship in self.ships:
            ship.join()
    def get_name(self):
        return self.city_name
if __name__ == '__main__':
    cc.start()