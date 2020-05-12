import heapq

def manhattan_distance(object,target):
    return abs(target[1]-object[1]) + abs (target[0]-object[0])
def verifiy_position (position):
    x_pos,y_pos = position
    return x_pos >= 0 and x_pos < 20 and y_pos >= 0 and y_pos < 20


def a_star (start,target,obtacle,hereustique = manhattan_distance):

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
    heapq.heappush(frontiere,(manhattan_distance(start,target),start))
    while len(frontiere) != 0 :
        value,current_position = heapq.heappop(frontiere)
        new_value = visited[current_position][0]+1
        if current_position == target:
            return get_path(target)
        x_pos , y_pos = current_position
        reserve = [(x_pos, y_pos+1), (x_pos+1, y_pos), (x_pos, y_pos-1), (x_pos-1, y_pos)]

        for pos in reserve :
            if pos not in obtacle and (pos not in visited or visited[pos][0]>new_value) and verifiy_position(pos):
                heapq.heappush(frontiere,(manhattan_distance(pos,target),pos))
                visited[pos] = (new_value,current_position)





