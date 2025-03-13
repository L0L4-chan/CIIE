def scale_coordinates(coords, original_size, new_size):
    ox, oy = original_size
    nx, ny = new_size
    
    scale_x = nx / ox
    scale_y = ny / oy
    
    scaled_coords = [
        [int(x * scale_x), int(y * scale_y)] for x, y in coords
    ]
    
    return scaled_coords

original_size = (2560,5040)
new_size = (1280,2520)

devil=  [[492,403], [2231,465]]
ghost= [[772,406], [853,956]]
bat=[[1259,489]]
boss= [[1268,1325]]


scaled_ghost_coords = scale_coordinates(bat, original_size, new_size)

print("bat: [")
for coord in scaled_ghost_coords:
    print(coord,",")
    scaled_ghost_coords = scale_coordinates(devil, original_size, new_size)

print("], devil : [")
for coord in scaled_ghost_coords:
    print(coord,",")
    
scaled_ghost_coords = scale_coordinates(ghost, original_size, new_size)

print("], ghost:[")
for coord in scaled_ghost_coords:
    print(coord,",")
    
print("], boss :[")

scaled_ghost_coords = scale_coordinates(boss, original_size, new_size)
for coord in scaled_ghost_coords:
    print(coord,",")
print("]")