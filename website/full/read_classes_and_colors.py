
def ClassesAndColors(class_file = 'coco_classes.txt', color_file ='color_pans.txt'):
    
    with open(class_file, 'r') as file:
        classes = [line.strip() for line in file.readlines()]
    # Main loop to capture and stream frames
    
    # Initialize an empty list to store colors
    colors = []

    # Read each line from the file
    with open(color_file, 'r') as file:
        lines = file.readlines()

    # Parse RGB values from each line and append to the colors list
    for line in lines:
        # Strip whitespace and split by comma
        rgb_values_str = line.split(',') 
        # Convert each substring to integer and append to the colors list
            
        if len(rgb_values_str) == 4:
            cols = rgb_values_str[:3]
            rgb_values = tuple(map(int, cols)) 
            colors.append(rgb_values)
    return classes, colors