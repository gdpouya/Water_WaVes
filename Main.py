import threading

cities=["BARCELONA","MARSEILLE","GENOA","NAPLES","MESSINA"]
class Ship(threading.Thread):
    def __init__(self,city,id,minimum) -> None:
        self.operator_semaphore = threading.Semaphore(1)
        self.moving=False
        self.boxes_check_semaphore = threading.Semaphore(1)
        self.ship_id=cities[city]+'_'+id
        self.minimum=minimum
        self.city=city
        self.boxes=0
    def run(self):
        while(self.boxes +  self.minimum or cities[city+1] < 1):
            self.boxes_check_semaphore.acquire()

class city():
    def __init__( self , city,ship_number , storage) :
        self.name=cities[city]
        self.ships = []
        self.ship_in_city=ship_number
        for i in range (0,ship_number):
            self.ships.append(Ship(city,i,storage))
    
    