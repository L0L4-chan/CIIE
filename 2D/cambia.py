def scale_coordinates(coords, original_size, new_size):
    ox, oy = original_size
    nx, ny = new_size
    
    scale_x = nx / ox
    scale_y = ny / oy
    
    scaled_coords = [
        [int(x * scale_x), int(y * scale_y)] for x, y in coords
    ]
    
    return scaled_coords

original_size = (5120,2160)
new_size = (2880,1215)

bat =  [[2222, 1813],[ 2795,1565] ]
    


scaled_ghost_coords = scale_coordinates(bat, original_size, new_size)


for coord in scaled_ghost_coords:
    
    print(coord,",")
   