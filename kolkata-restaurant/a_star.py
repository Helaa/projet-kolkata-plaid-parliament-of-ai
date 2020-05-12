import heapq

def manhattan_distance(pos,target):
    assert len(target) == 2
    assert len(pos) == 2

    return abs(target[1]-pos[1]) + abs (target[0]-pos[0])

def euc_dist(pos, target):
    assert len(target) == 2
    assert len(pos) == 2

    return ( (target[0] - pos[0]) ** 2 + (target[1] - pos[1]) ** 2 ) ** 0.5

def custom_dist(start, pos, target):
    assert len(target) == 2
    assert len(pos) == 2

    dx1 = pos[0] - target[0]
    dy1 = pos[1] - target[1]

    dx2 = start[0] - target[0]
    dy2 = start[1] - target[1]

    return abs(dx1*dy2 - dx2*dy1)

def verifiy_position (position, lines, cols):
    assert len(position) == 2

    x_pos,y_pos = position
    
    return x_pos >= 0 and x_pos < lines and y_pos >= 0 and y_pos < cols


def a_star(start, target, obtacle, lines=20, cols=20, hereustique = manhattan_distance):

    def get_path(target):
        i = target
        path = [target]
        while i != start:
            i = visited[i][1]
            path.append(i)
        path.reverse()
        return path


    visited = {}
    visited[start] = (0,None)
    frontiere = []
    heapq.heappush(frontiere,(hereustique(start,target),start))
    while len(frontiere) != 0 :
        value,current_position = heapq.heappop(frontiere)
        new_value = visited[current_position][0]+1
        if current_position == target:
            return get_path(target)
        x_pos , y_pos = current_position
        reserve = [(x_pos, y_pos+1), (x_pos+1, y_pos), (x_pos, y_pos-1), (x_pos-1, y_pos)]

        for pos in reserve :
            if pos not in obtacle and (pos not in visited or visited[pos][0]>new_value) and verifiy_position(pos, lines, cols):
                heapq.heappush(frontiere,(hereustique(pos,target),pos))
                visited[pos] = (new_value,current_position)


def test():
    lines = 4
    cols = 6
    # matrix of lines=lines and cols=cols

    start = (9, 11)
    target = (8, 10)
    obstacles = [(4, 5), (4, 8), (4, 11), (4, 14), (5, 5), (5, 8), (5, 11), (5, 14),
                 (6, 5), (6, 8), (6, 11), (6, 14), (7, 5), (7, 8), (7, 11), (7, 14),
                 (8, 5), (8, 8), (8, 11), (8, 14), (9, 5), (9, 6), (9, 7), (9, 8), 
                 (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (10, 5), (10, 6),
                 (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14),
                 (11, 5), (11, 8), (11, 11), (11, 14), (12, 5), (12, 8), (12, 11), (12, 14),
                 (13, 5), (13, 8), (13, 11), (13, 14), (14, 5), (14, 8), (14, 11), (14, 14),
                 (15, 5), (15, 8), (15, 11), (15, 14)]

    path = a_star (start,target,obstacles, lines, cols, hereustique = euc_dist)
    print(path)


test()

