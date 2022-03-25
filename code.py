import random

flights = ['A112','B112']
book_id = {}

class Flight:

    business = []
    economy = []
    name = ""
#Reading data from file and separating rows, columns and kinds of seat(W - window, M - Middle, A - Aisle)
    def __init__(self, filename):
        self.name = filename[:-4]
        file = open(filename)
        lines = file.readlines()
        for line in lines:
            line = line.split()
            _class = line[0]
            _rows = int(line[-1])

            ori = ""
            for ele in line[2:5]:
                ori += ele
            
            ori = ori[1:-2]
            ori = list(map(int, ori.split(',')))

            if(_class == "Business"):
                # print(_rows)
                s = "M"*ori[0] + " " + "M"*ori[1] + " " + "M"*ori[2]
                s = [s for i in range(_rows)]
                for x in range(len(s)):
                    s[x] = 'W' + s[x][1:-1] + 'W'
                    s[x] = s[x].replace('M M', 'A A')
                self.business = s
            
            elif(_class == "Economy"):
                # print(_rows)
                s = "M"*ori[0] + " " + "M"*ori[1] + " " + "M"*ori[2]
                s = [s for i in range(_rows)]
                for x in range(len(s)):
                    s[x] = 'W' + s[x][1:-1] + 'W'
                    s[x] = s[x].replace('M M', 'A A')
                self.economy = s
            
#printing seat details
    def printbusiness(self):
        for ele in self.business:
            print(ele)
        print("B: Booked")
        print("A: Aisle")
        print("M: Middle")
        print("W: Window")
    
    def printeconomy(self):
        for ele in self.economy:
            print(ele)
        print("B: Booked")
        print("A: Aisle")
        print("M: Middle")
        print("W: Window")

#Booking seats
    def book_seat(self, seat, div):
        row, col = seat.split("_")
        col = ord(col)-64
        row = int(row)
        print(row, col)

        seats = []
        if(div == 'Business'):
            seats = self.business
        elif(div == 'Economy'):
            seats = self.economy
        count = -1
        for i in range(len(seats[row-1])):
            if seats[row-1][i] != ' ':
                count += 1
            if seats[row-1][i] == ' ':
                continue
            if count == col-1:
                if seats[row-1][count] == 'B':
                    print("Seat already booked")
                    break
                seatType = seats[row-1][i] 
                seats[row-1] = seats[row-1][:i] + 'B' + seats[row-1][i+1:]
                rn = random.randint(100,300)
                if(self.name in book_id.keys()):
                    name = input("Enter the name of the passenger: ")
                    book_id[self.name].append({rn: [row,i,{"name":name}]})
                else:
                    name = input("Enter the name of the passenger: ")
                    book_id[self.name] = [{rn: [row,i,{"name":name}],}]
                break
        
        if(div == 'Business'):
            self.business = seats
        elif(div == 'Economy'):
            self.economy = seats

        return (seatType)    

           
                
class Person:
    #Base price of an Economy Class ticket is INR 1000 and for Business Class it is INR 2000.
    #Aisle and Window seats will cost INR 100 more
    cost = {
        "Economy" : {
            "M" : 1000,
            "A" : 1100,
            "W" : 1100
        },
        "Business" : {
            "M" : 2000,
            "A" : 2100, 
            "W" : 2100
        },
    }

    totalCost = 0

    #Surge pricing : After each successful booking, price of the ticket increases by INR
    #100 for Economy class and INR 200 for Business class on successive booking    
    def updatecost(self, div,seatType):
        self.totalCost += self.cost[div][seatType]
        amount = 100 if div == "Economy" else 200
        self.cost[div]["M"] += amount
        self.cost[div]["A"] = self.cost[div]["A"] + amount
        self.cost[div]["W"] = self.cost[div]["W"] + amount
        print("Total Cost : ",self.totalCost)

    def book(self, flights,flight_name,seat_num,seat_class):
        for flight in flights:
            if flight.name == flight_name:
                seatType = flight.book_seat(seat_num, seat_class)
                if seat_class == "Business":
                    print(flight.printbusiness())
                else:
                    print(flight.printeconomy())
                if(seatType=="B"):
                    print("seat already booked")
                    return False
                    break
                self.updatecost(seat_class,seatType)
                return True
                break

    def bookMeal(self,no):
        self.totalCost+=(no*200)


flights = [Flight(name + ".txt") for name in flights]

while(True):
    #Displaying available flights
    print("List of available flights : ")
    for i in flights:
        print(i.name)


    flight_name = input("Enter the flight name from the available list: ")
    print()
    for i in flights:
        if(flight_name == i.name):
            current_flight = i

    #Displaying seats
    print()
    print("-----------------------------------------")
    print("Economy Class Seats : ")
    i.printeconomy()
    print()
    print("Business Class Seats : ")
    i.printbusiness()
    print("-----------------------------------------")
    print()

    #Asking for user inputs in seat booking
    noOfSeats = int(input("Enter the no of seats : "))

    seat_class = input("Enter the class : (Business/Economy) ")

    person = Person()

    for i in range(noOfSeats):
        seatNo = input("Enter the seat number ex(5_F) : ")
        if(person.book(flights,current_flight.name,seatNo,seat_class)):
            continue
        else:
            noOfSeats+=1
            seatNo = input("Enter the seat number ex(5_F) : ")

    #Meal Option
    wantMeal = input("want meal for every passenger(Y/N)?:")

    if(wantMeal=="Y"):
        person.bookMeal(noOfSeats)
    print()
    print("Total Cost with/without meal = ",person.totalCost)


    #Print individual and flight summary for all the bookings
    for i in book_id.keys():
        print("Flight Name : ",i)
        print()
        for j in book_id[i]:
            for key, value in j.items():
                print("Booking ID : ",key)
                print("Seat Number : ",value[0] , (value[1]))
                print("Name : ",value[-1]["name"])
                print()

    ip = input("Want to continue the booking : (Y,N)?")

    if(ip=="N"):
        break
