'''
cars with random amount of coal
sort cars
override operators <=> for binary search
create class list of cars
sorting algorithm Bubble, insertion sorting algorithm
method of binary search of a car with certain amount of coal
'''


from random import randint, choice


class Car:
    def __init__(self, coal, serial):
        self.serial = serial
        self.coal = coal

    def __repr__(self):
        return f'Car #{self.serial} has {self.coal} ton of coal'

    #Only for binary search for coal
    def __eq__(self, another):
        return self.coal == another
    
    def __gt__(self, another):
        return self.coal > another
    
    def __lt__(self, another):
        return self.coal < another
    
    def __ge__(self, another):
        return self.coal >= another
    
    def __le__(self, another):
        return self.coal <= another
    
    def __ne__(self, another):
        return self.coal != another


class Train:
    def __init__(self, cars):
        self.cars = [Car(randint(1,74), randint(1,1000)) for x in range(cars)]

    def __repr__(self):
        text = f'This is a train with {len(self.cars)} cars: '
        for x in self.cars:
            text += '\n\t' + str(x)
        return text

    def add_car(self, item, num):
        if item == 'coal':
            car = Car(num, randint(1,1000))
        else:
            car = Car(randint(1,74), num)
        self.cars.append(car)
        return car
            
    #bubble sort
    def bubble_sort_to_right(self, param = True):
        param = 'coal' if param else 'serial'
        for x in range (len(self.cars)-1, 0, -1):
            end = True
            for y in range (x):
                if getattr(self.cars[y],param) > getattr(self.cars[y+1], param):               
                    self.cars[y],self.cars[y+1] = self.cars[y+1], \
                    self.cars[y]
                    end = False
            if end:
                break

    def bubble_sort_to_left(self, param = True):
        param = 'coal' if param else 'serial'
        for x in range (len(self.cars)-1):                
            end = True
            for y in range (len(self.cars)-x-1):
                if getattr(self.cars[y], param) < getattr(
                    self.cars[y+1], param):
                    
                    self.cars[y],self.cars[y+1] = self.cars[y+1], \
                    self.cars[y]
                    end = False
            if end: break
            
    #insertion sort
    def insertion_sort_to_right(self, param = True):

        param = 'coal' if param else 'serial'
        
        for x in range(1, len(self.cars)):
            current_car = self.cars[x]
            index = x - 1

            while getattr(current_car, param )< getattr(self.cars[
                index], param) and index >= 0:              #to right
                self.cars[index+1] = self.cars[index]
                index -= 1
            self.cars[index+1] = current_car

    def insertion_sort_to_left(self, param = True):
        param = 'coal' if param else 'serial'
        for x in range(1, len(self.cars)):
            current_car = self.cars[x]
            index = x - 1

            while getattr(current_car, param) > getattr(
                self.cars[index], param) and index >= 0:    #to left
                self.cars[index+1] = self.cars[index]
                index -= 1
            self.cars[index+1] = current_car                        

    #selection sort
    def select_sort_to_right(self, param = True):
        param = 'coal' if param else 'serial'
        for i in range(len(self.cars)-1):
            minindex = i
            for j in range(i+1, len(self.cars)):
                if getattr(self.cars[j], param) < getattr(
                    self.cars[minindex], param):
                    minindex = j
            if minindex != i:
                self.cars[minindex], self.cars[i] = \
                                       self.cars[i], self.cars[minindex]

    def select_sort_to_left(self, param = True):
        param = 'coal' if param else 'serial'
        for i in range(len(self.cars)-1):
            minindex = i
            for j in range(i+1, len(self.cars)):
                if getattr(self.cars[j], param) > getattr(
                    self.cars[minindex], param):
                    minindex = j
            if minindex != i:
                self.cars[minindex], self.cars[i] = \
                                       self.cars[i], self.cars[minindex]
        
    #binary search
    def binary_search_to_right(self, value):
        high = len(self.cars)-1
        low = 0

        while low <= high:
            mid = (high + low) // 2
            if self.cars[mid] == value:
                return self.cars[mid]
            elif self.cars[mid] > value:                #to right
                high = mid - 1
            else:
                low = mid + 1
        return False

    def binary_search_to_left(self, value):
        high = len(self.cars)-1
        low = 0

        while low <= high:
            mid = (high + low) // 2
            if self.cars[mid] == value:
                return self.cars[mid]
            
            elif self.cars[mid] < value:                #to left
                high = mid - 1
            else:
                low = mid + 1
        return False
    
    def find_sn(self, value):
        self.insertion_sort_to_right(0)        
        high = len(self.cars)-1
        low = 0

        while low <= high:
            mid = (high + low) // 2
            if self.cars[mid].serial == value:
                return self.cars[mid]
            
            elif self.cars[mid].serial > value:         #to right
                high = mid - 1
            else:
                low = mid + 1
        return False

    def find(self, value, side = True):
        if side:
            sorter = choice([self.select_sort_to_right,
                             self.insertion_sort_to_right,
                             self.bubble_sort_to_right])
            sorter()
            return self.binary_search_to_right(value)
        
        else:
            sorter = choice([self.select_sort_to_left,
                             self.insertion_sort_to_left,
                             self.bubble_sort_to_left])
            sorter()
            return self.binary_search_to_left(value)      

    def find_by_type(self, value, mytype):
        if mytype == 'coal':
            return self.find(value)
        elif mytype == 'serial':
            return self.find_sn(value)
        else:
            try:
                return self.cars[value]
            except IndexError:
                return False

    def destroy(self, car):
        self.cars.remove(car)
        return car


class Depot:
    train = False

    @classmethod
    def generate(cls, value):
        cls.train = Train(value)

    @classmethod
    def boom(cls):
        cls.train = False





            
