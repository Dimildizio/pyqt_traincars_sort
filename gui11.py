from PyQt4 import QtGui, QtCore
import sys
import os
from cars_coal import *




class MainWindow(QtGui.QMainWindow): 
    def __init__(self):
        super().__init__()
        self.buttons = {'Show':[self.go_train, 'Show the whole train'],
                       'Cars':[self.go_cars, 'Manipulate cars'],
                       'Arrange':[self.go_sort, 'Sort cars in orded'],
                       'Destroy':[self.boom, 'Boom!'],
                       'Exit':[self.close_me, 'Close the application']}
        self.name = 'Train'
        self.setWindowIcon(QtGui.QIcon('pics\\bullet_train.ico'))
        self.picture = 'pics\\trainsteam.jpg'
        self.setGeometry(500,150,260,450)
        self.setWindowTitle('Trains')
        self.setMaximumSize(300,450)
        self.style = QtGui.QApplication.setStyle(
            QtGui.QStyleFactory.create('Plastique'))
        
        #create status bar
        self.statusBar()
        
        #exit submenu
        exit_me = QtGui.QAction('&Exit me', self)
        exit_me.setShortcut('Ctrl+Q')
        exit_me.setStatusTip('Leave the App')
        exit_me.triggered.connect(self.close_me)

        #create mainmenu panel
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(exit_me)
        fileMenu.addSeparator()
        self.home()

    def home(self):

        v_box = QtGui.QVBoxLayout()

        #top label
        label = QtGui.QLabel(self.name)
        font = QtGui.QFont('Times', 14)
        font.setBold(1)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        v_box.addWidget(label)
        
        #picture
        pic = QtGui.QLabel()
        pic.setMinimumSize(QtCore.QSize(100, 50))
        pic.setSizeIncrement(QtCore.QSize(1, 1))
        pic.setBaseSize(QtCore.QSize(300, 200))
        pic.setPixmap(QtGui.QPixmap(self.picture))
        pic.setScaledContents(True)
        v_box.addWidget(pic)

        #buttons
        for key,value in self.buttons.items():
            btn = QtGui.QPushButton(key)
            btn.clicked.connect(value[0])
            btn.setStatusTip(value[1])
            v_box.addWidget(btn)

        #initialize everything above
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(v_box)
        self.setCentralWidget(centralWidget)
        
        self.show()

    def go_cars(self):
        self.close()
        self.window = CarWindow()

    def go_train(self):
        self.close()
        self.window = A_Train()

    def go_home(self):
        self.close()
        self.window = MainWindow()

    def go_sort(self):
        self.close()
        self.window = CarSort()

    def go_generate(self):
        self.close()
        self.window = GeneratorWindow()

    def i_message(self, icon, title, text):
        msgBox = QtGui.QMessageBox(
            icon, title, text, buttons = QtGui.QMessageBox.Ok)
        return msgBox.exec_()

    def close_me(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText('Are you sure you want to exit?')
        msgBox.setWindowTitle('Exit')
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.addButton(QtGui.QPushButton('Yes'), QtGui.QMessageBox.YesRole)
        msgBox.addButton(QtGui.QPushButton('No'), QtGui.QMessageBox.NoRole)
        myexit = msgBox.exec_()
        
        if not myexit:
            sys.exit()
        
    def boom(self):
        self.i_message(QtGui.QMessageBox.Information, 'Boom!',
                       'Your train has been destroyed')
        Depot.train = False
        self.go_generate()


class GeneratorWindow(MainWindow):
    def __init__(self):
        super().__init__()
        self.buttons = {'Generate':[self.get_train, 'Generate a train'],
                        'Exit':[self.close_me, 'Close the application']}
        self.name = 'Welcome to the train manager!\nDo you wish to create a train?'
        self.picture = 'pics\\facttrain.jpg'

        self.home()

    def get_train(self):
        num, ok = QtGui.QInputDialog.getInt(
                self, 'Generating train', 'How many cars?')
        if ok:                
            if num > 5000:
                self.i_message(QtGui.QMessageBox.Warning,
                               'You\'ve been rejected',
                               "You've requested too many cars")            
            elif num < 1:
                self.i_message(QtGui.QMessageBox.Warning,
                               'You\'ve been rejected',
                               "There is no point for you in train without cars")           
            else:         
                Depot.generate(num)
                self.go_home()

                
class CarSort(MainWindow):
    def __init__(self, train = False):
        super().__init__()
        self.setGeometry(500,150,300,450)
        self.picture = 'pics\\Aurora610.jpg'
        self.name = 'Arrange the cars'
        msgBox = QtGui.QMessageBox()
        msgBox.setText('              Sort direction?')         #setAlignment?
        msgBox.setWindowTitle('Sorting')
        msgBox.addButton(QtGui.QPushButton('From left to right'), QtGui.QMessageBox.YesRole)
        msgBox.addButton(QtGui.QPushButton('From right to left'), QtGui.QMessageBox.NoRole)
        self.direction = msgBox.exec_()
        
        msgBox1 = QtGui.QMessageBox()
        msgBox1.setText('              Sort parameter?')         #setAlignment?
        msgBox1.setWindowTitle('Sorting')
        msgBox1.addButton(QtGui.QPushButton('Serial number'), QtGui.QMessageBox.YesRole)
        msgBox1.addButton(QtGui.QPushButton('Quantity of coal'), QtGui.QMessageBox.NoRole)
        self.param = msgBox1.exec_()
        
        self.buttons = {'Home':[self.go_home, 'Go to the main page'],
                        'Bubble sort':[self.call_bubble, 'Bubble sorting algorithm'],
                        'Selection sort':[self.call_selection, 'Selection sorting algorithm'],
                        'Insertion sort':[self.call_insertion, 'Insertion sorting algorithm'],
                        'Exit':[self.close_me, 'Close the application']}

        self.home()

    @property
    def i_msg(self):
        self.i_message(QtGui.QMessageBox.Information,
                       'Sorted completed',
                       'Cars have been arranged in order')
           
    def call_selection(self):
        self.i_msg
        if self.direction:
            return Depot.train.select_sort_to_left(self.param)
        return Depot.train.select_sort_to_right(self.param)
    
    def call_bubble(self):
        self.i_msg
        if self.direction:
            return Depot.train.bubble_sort_to_left(self.param)
        return Depot.train.bubble_sort_to_right(self.param)
    
    def call_insertion(self):
        self.i_msg
        if self.direction:
            return Depot.train.insertion_sort_to_left(self.param)
        return Depot.train.insertion_sort_to_right(self.param)


class CarWindow(MainWindow):
    def __init__(self, train = False):
        super().__init__()
        self.picture = 'pics\\steam_train.jpg'
        self.name = 'Cars'
        self.buttons = {'Home':[self.go_home, 'Go to the main page'],
                       'Add a car':[self.add_car, 'Add more cars'],
                       'Find a car':[self.find_car, 'Search for a car'],
                       'Remove a car':[self.remove_car, 'Delete a car'],
                       'Exit':[self.close_me, 'Close the application']}
        self.home()

    def find_car(self):
        car = self.search()
        if car:
            self.close()
            self.window = A_Car(car)

    def search(self):
        items = ('serial','coal', 'index')

                                            #dialog items
        item, ok = QtGui.QInputDialog.getItem(
            self, 'Find a car', 'Find by', items, 0, False)
        if ok:
                                            #dialog digits
            num, ok = QtGui.QInputDialog.getInt(
                self, 'Finding', 'Input a digit')
            car = Depot.train.find_by_type(num, item)
            if car:
                return car
            else:
                self.i_message(QtGui.QMessageBox.Information,
                               'Ooops', 'Car not found')

    def remove_car(self):  
        sn = self.search()
        if sn:
            text = f'Car {sn.serial} disconnected from the train'
            Depot.train.cars.remove(sn)
            self.i_message(QtGui.QMessageBox.Information,
                           'Car removed', text)
        if len(Depot.train.cars) < 1:
            self.i_message(QtGui.QMessageBox.Critical,
                           'Train confiscated',
                           'You don\'t have any cars left\nYour tain has been confiscated')
            
            self.go_generate()
            return
                        
    def add_car(self):
        items = ('serial number','coal')
        item, ok = QtGui.QInputDialog.getItem(
            self, 'Connecting a car', 'Add by', items, 0, False)
        if ok:
            num, okay = QtGui.QInputDialog.getInt(
                self, 'Connecting a car', 'Input a digit')
            if okay:
                car = Depot.train.add_car(item, num)
                
                text = f'Car {car.serial} with {car.coal} coal connected to the train'
                self.i_message(QtGui.QMessageBox.Information,
                               'Car added', text)


    
class A_Car(MainWindow):
    def __init__(self, car = True):
        self.car = car
        super().__init__()
        self.setGeometry(500,150,200,400)
        self.picture = 'pics\\steamtrain.jpg'
        self.buttons = {'Home':[self.go_home,
                                'Go to the main page']}


        self.home()
                 

    def home(self):
        v_box = QtGui.QVBoxLayout()

        #top label
        label = QtGui.QLabel('Search result')
        font = QtGui.QFont('Times', 14)
        font.setBold(1)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        v_box.addWidget(label)
        
        #picture
        pic = QtGui.QLabel()
        pic.setMinimumSize(QtCore.QSize(100, 50))
        pic.setSizeIncrement(QtCore.QSize(1, 1))
        pic.setBaseSize(QtCore.QSize(200, 50))
        pic.setPixmap(QtGui.QPixmap(self.picture))
        pic.setScaledContents(True)
        v_box.addWidget(pic)

        #text
        label_1 = QtGui.QLabel(str(self.car))
        font = QtGui.QFont('Times', 12)
        label_1.setFont(font)
        label_1.setAlignment(QtCore.Qt.AlignCenter)
        v_box.addWidget(label_1)

        #button
        for key,value in self.buttons.items():
            btn = QtGui.QPushButton(key)
            btn.clicked.connect(value[0])
            btn.setStatusTip(value[1])
            v_box.addWidget(btn)


        #initialize everything above
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(v_box)
        self.setCentralWidget(centralWidget)
        
        self.show()

class A_Train(A_Car):
    def __init__(self, car = True):
        super().__init__()
        self.picture = 'pics\\chocho.jpg'
        self.name = 'This is your train'
        self.setGeometry(500,150,250,200)
        self.car = car

        self.home()

    def home(self):
        v_box = QtGui.QVBoxLayout()

        #top label
        label = QtGui.QLabel(self.name)
        font = QtGui.QFont('Times', 14)
        font.setBold(1)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        v_box.addWidget(label)

        #picture
        pic = QtGui.QLabel()
        pic.setMinimumSize(QtCore.QSize(100, 50))
        pic.setSizeIncrement(QtCore.QSize(1, 1))
        pic.setBaseSize(QtCore.QSize(200, 50))
        pic.setPixmap(QtGui.QPixmap(self.picture))
        pic.setScaledContents(True)
        v_box.addWidget(pic)

        #text
        edit = QtGui.QTextEdit()
        edit.setText(str(Depot.train))
        edit.setReadOnly(True)
        edit.setMinimumSize(QtCore.QSize(100, 200))
        v_box.addWidget(edit)

        #buttons
        for key,value in self.buttons.items():
            btn = QtGui.QPushButton(key)
            btn.clicked.connect(value[0])
            btn.setStatusTip(value[1])
            v_box.addWidget(btn)


        #initialize everything above
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(v_box)
        self.setCentralWidget(centralWidget)
        
        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GeneratorWindow()
    sys.exit(app.exec())
