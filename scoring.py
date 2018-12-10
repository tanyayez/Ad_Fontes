def get_distance(coord1, coord2):
    #print("function entered!")
    return abs(coord1[0]-coord2[0]) + abs(coord1[1] - coord2[1])

def get_points(data, rides):
    score = 0
    #print("new car: ")
    current = tuple([0, 0])
    s = 0
    for ride in rides:
        #print(data[ride])
        s += get_distance(current, data[ride][2])
        #print("S: ", s, data[ride][0])
        if data[ride][0] >= s:
            #print("ride started on time: ", s)
            score += bonus
        score += data[ride][4]
        current = data[ride][3]
    #print("This car earned: ", score)
    return score


def points_for_file(infile, outfile):
    global bonus
    global steps

    file = open(infile)
    info = file.readline().split()
    bonus = int(info[4])
    steps = int(info[5])

    data = dict()
    index = 0
    for line in file.readlines():
        # data[ride index] = [start time, end time, startcoords(x, y), endcoords(x,y), distance]
        temp = line.split()
        distance = abs(int(temp[0]) - int(temp[2])) + abs(int(temp[1]) - int(temp[3]))
        data[str(index)] = [int(temp[4]), int(temp[5]), tuple([int(temp[0]), int(temp[1])]),
                            tuple([int(temp[2]), int(temp[3])]), int(distance)]
        index += 1

    file.close()

    points = 0

    file = open(outfile)
    for line in file.readlines():
        points += get_points(data, line.split()[1:])

    print(infile, outfile, "    ", points)
    return points

def main():

    total_score = 0

    infile = 'example.in'
    outfile = 'a_res.out'
    total_score += points_for_file(infile, outfile)


    infile = 'should_be_easy.in'
    outfile = 'b_res.out'
    total_score += points_for_file(infile, outfile)


    infile = 'c_no_hurry.in'
    outfile = 'c_res.out'
    total_score += points_for_file(infile, outfile)


    infile = 'd_metropolis.in'
    outfile = 'd_metropolis.out'
    total_score += points_for_file(infile, outfile)


    infile = 'e_high_bonus.in'
    outfile = 'e_res.out'
    total_score += points_for_file(infile, outfile)

    print("Total for this submission: ", total_score)
    return total_score

if __name__ == "__main__":
    main()