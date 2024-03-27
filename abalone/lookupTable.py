LEGAL_VECTORS = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0)]


def all_coords():
    """An iterator through all coordinate points on the board in row-major order. Coordinates expressed as (x, y) tuples."""
    for y in range(1, 10):
        start = y-4 if y-4 > 1 else 1
        end = y+4 if y+4 < 9 else 9
        for x in range(start, end+1):

            yield (x, y)

def sum_tuples(a, b):
        """Sums all the entries in the given tuples"""
        return tuple(map(lambda x, y: x+y, a, b))

def get_adjacent_spaces(coord):
    """Returns a list containing coordinates for all spaces immediately adjacent to the given coordinates"""

    return list([sum_tuples(coord, vector) for vector in LEGAL_VECTORS])

def coord_in_board(coord):
        """Returns true or false whether or not the given tuple is a valid board coordinate.
        Assumes that the coordinate is an integer tuple with two values"""
        x,y = coord
        return (1<=x<=9) and (1<=y<=9) and (y-4 <= x <= y+4)

def index(coord):
        if not coord_in_board(coord):
            return -1

        x,y = coord
        return ([0, 5, 11, 18, 26, 35, 43, 50, 56][y-1] + x - 1 - (y-5 if y-5 > 0 else 0))

def main():
    coord = (1,1)
    #print(coord, index(coord))   
    #print(sum_tuples(coord, (0,1)),  index(sum_tuples(coord, (0,1))))     
    
    print("{", end="")
    for i, coord in enumerate(all_coords()):
        

        theend = "},\n"
        if i == 60:
            theend = "}"
        print("{", end = "")
        print(*[index(adjacent) for adjacent in get_adjacent_spaces(coord) ], end=theend, sep=", ")
    
    
    print("}")


if __name__ == "__main__":
    main()