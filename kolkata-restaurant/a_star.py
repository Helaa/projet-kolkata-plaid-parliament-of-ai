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


def a_star (start, target, obtacle, lines=20, cols=20, hereustique = manhattan_distance):

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
    from itertools import product
    
    lines = 4
    cols = 6
    # matrix of lines=lines and cols=cols
    
    start = (2, 0)
    target = (0, 5)
    obstacles = [(0,4), (1,4), (2,4)]

    path = a_star (start,target,obstacles, lines, cols, hereustique = euc_dist)
    print(path)


test()

