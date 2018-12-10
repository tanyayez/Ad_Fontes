files = ["DataIn/a_example.in", "DataIn/b_should_be_easy.in", "DataIn/c_no_hurry.in", "DataIn/d_metropolis.in",
         "DataIn/e_high_bonus.in"]


class City:
    def __init__(self):
        self.n_of_cars = 0
        self.rows = 0
        self.col = 0
        self.n_of_rides = 0
        self.bonus = 0
        self.steps = 0
        self.cars = []
        self.map = []

    def read_from_file(self, name):
        i = 0
        with open(name, 'r', encoding='utf-8') as infile:
            for line in infile:
                if i == 0:
                    a = line.split()
                    self.rows = int(a[0])
                    self.col = int(a[1])
                    self.n_of_cars = int(a[2])
                    self.n_of_rides = int(a[3])
                    self.bonus = int(a[4])
                    self.steps = int(a[5])
                    i += 1
                else:
                    a = line.split()
                    ride = Ride((int(a[0]), int(a[1])), (int(a[2]), int(a[3])), int(a[4]), int(a[5]))
                    ride.ind = i - 1

                    self.map.append(ride)
                    i += 1

        for j in range(self.n_of_cars):
            car = Car(j + 1)
            self.cars.append(car)

    def simulation(self):
        # sort rides by lenght

        self.map.sort(key=lambda ride: ride.lenght_ride(), reverse= True)

        for t in range(self.steps):
            for car in self.cars:
                if car.is_free(t):

                    ride = car.get_new_ride(self.map, t, self.n_of_rides)
                    if ride != False:
                        car.assing_ride(ride, t)
                        ##   delete ride from list of rides
                        del self.map[self.map.index(ride)]
                        # print("Ride" + str(ride.ind) + "  assinged and deleted " + "   to the car " + str(car.my_ind))

    def validate(self):
        check = dict()
        for car in city.cars:
            curr = 0
            curr_pos = (0, 0)
            for ride in car.all_ride_ind:
                if ride.ind not in check.keys():
                    check[ride.ind] = [car]
                else:
                    check[ride.ind].append(car)
                time = City.distance_to(curr_pos, ride.start) + ride.lenght_ride()
                if time > ride.l_fin:
                    print("Not valid")
                    return False
                else:
                    curr_pos = ride.end

        for key in check.keys():
            if len(check[key]) > 1:
                print("Not valid")
                return False

        print("Brilliant solution!")
        return True

    @staticmethod
    def distance_to(start, end):
        return abs(int(start[0]) - int(end[0])) + abs(int(start[1]) - int(end[1]))

    def write_result(self, name):
        with open(name, 'w') as file:
            for car in self.cars:
                text = str(car.my_ind) + ' '
                for ride in car.all_ride_ind:
                    text += str(ride.ind) + ' '
                text += "\n"
                file.write(text)

    def toStr(self):
        print("Rows  " + str(self.rows) + "  Col " + str(self.col) + "  N cars " + str(self.cars) + "  N rides " + str(
            self.rides) + " Bonus " + str(self.bonus) + "  Steps  " + str(self.steps))


class Car:
    def __init__(self, ind):
        self.my_ind = ind
        self.cur_coord = (0, 0)
        self.end_t_ride = None
        self.free = True
        self.all_ride_ind = []

    def is_free(self, cur_simulat_t):
        if self.free == False:
            if self.end_t_ride == cur_simulat_t:
                self.free = True
                return True
            else:
                return False

        return True

    def assing_ride(self, ride, cur_time):
        self.free = False
        self.end_t_ride = cur_time + self.distance_to(ride.start) + ride.lenght_ride()
        self.cur_coord = ride.end
        self.all_ride_ind.append(ride)

    def get_new_ride(self, city_map, cur_t, n_rides):

        l = len(city_map)
        if n_rides // 3 > l:
            parts = [city_map[:l//3], city_map[l//3:2*l//3], city_map[2*l//3:]]
            for part in parts:
                part.sort(key = lambda ride: ride.distance_to(self.cur_coord))
                for ride in part:
                    way_r = cur_t + self.distance_to(ride.start) + ride.lenght_ride()
                    if way_r <= ride.l_fin:
                        return ride
        else:
            for ride in city_map:
                way_r = cur_t + self.distance_to(ride.start) + ride.lenght_ride()
                if way_r <= ride.l_fin:
                    return ride


        print('Ride not found for car ' + str(self.my_ind) + '   at time ' + str(cur_t))
        return False

    def distance_to(self, end):
        return abs(int(self.cur_coord[0]) - int(end[0])) + abs(int(self.cur_coord[1]) - int(end[1]))


class Ride:
    def __init__(self, st, fin, e_st, l_fin):
        self.start = st
        self.end = fin
        self.e_st = e_st
        self.l_fin = l_fin
        self.ind = None

    def distance_to(self, p):
        return abs(int(self.start[0]) - int(p[0])) + abs(int(self.start[1]) - int(p[1]))

    def lenght_ride(self):
        return abs(int(self.start[0]) - int(self.end[0])) + abs(int(self.start[1]) - int(self.end[1]))

    def toStr(self):
        print("Ride " + str(self.ind) + "  Start  " + str(self.start) + "  End " + str(self.end) + "  Erl_st " + str(
            self.e_st) + "  L_fin  " + str(self.l_fin))


def main():
    city = City()
    city.read_from_file(files[1])
    city.simulation()
    res = city.validate()
    city.write_result('Longest_Rides_alg_Res/b_good_res.out')

