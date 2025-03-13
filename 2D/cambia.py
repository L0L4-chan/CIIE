def scale_coordinates(coords, original_size, new_size):
    ox, oy = original_size
    nx, ny = new_size
    
    scale_x = nx / ox
    scale_y = ny / oy
    
    scaled_coords = [
        [int(x * scale_x), int(y * scale_y)] for x, y in coords
    ]
    
    return scaled_coords

original_size = (6400,2160)
new_size = (2400,810)

ghost_coords = [[500, 1000], [1488,1994],[6105,1737],[800,1790],[687,1956],[5559,1880],[2830,1790]]


scaled_ghost_coords = scale_coordinates(ghost_coords, original_size, new_size)

print("Scaled Coordinates:")
for coord in scaled_ghost_coords:
    print(coord)