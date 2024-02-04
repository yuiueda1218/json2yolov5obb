import os
import math
import json

json_file_path = "YOURFILE.json"
out_path = "YOUR_OUTPUT_PATH"
false = "False"
null = "null"

# Please modify the contents.
class_mapping = {
    "abdomen": 0,
    "humerus": 1,
    "lung": 2,
    "mediastinum": 3,
    "spine": 4
}

# Function to rotate coordinates
def rotate_point(x_center, y_center, theta, x, y):
    x_rotated = x_center + (x - x_center) * math.cos(theta) - (y - y_center) * math.sin(theta)
    y_rotated = y_center + (x - x_center) * math.sin(theta) + (y - y_center) * math.cos(theta)
    return x_rotated, y_rotated

# Function to process annotation data and write to files
def process_annotations_to_files(annotation_json, out_path):
    for annotation in annotation_json:
        # Extracting the file name
        image_path = annotation["data"]["image"]
        file_name = image_path.split('/')[-1].replace('.jpg', '') + '.txt'
        full_file_path = os.path.join(out_path, file_name)

        # Opening the file
        with open(full_file_path, 'w') as file:
            for ann in annotation['annotations']:
                for result in ann['result']:
                    # Calculating basic parameters
                    original_width = result['original_width']
                    original_height = result['original_height']
                    value = result['value']
                    label = value['rectanglelabels'][0]
                    label_class = class_mapping[value['rectanglelabels'][0]]

                    # Calculating center coordinates, width, height, and rotation
                    x_center = value['x'] / 100 * original_width
                    y_center = value['y'] / 100 * original_height
                    width = value['width'] / 100 * original_width
                    height = value['height'] / 100 * original_height
                    rotation_radians = math.radians(value['rotation'])

                    # Coordinates of the corners (before rotation)
                    x_tl = x_center
                    y_tl = y_center
                    x_tr = x_center + width
                    y_tr = y_center
                    x_br = x_center + width
                    y_br = y_center + height
                    x_bl = x_center
                    y_bl = y_center + height

                    # Rotating the coordinates of the corners
                    x1, y1 = rotate_point(x_center, y_center, rotation_radians, x_tl, y_tl)
                    x2, y2 = rotate_point(x_center, y_center, rotation_radians, x_tr, y_tr)
                    x3, y3 = rotate_point(x_center, y_center, 

with open(json_file_path, 'r') as file:
    annotation_json = json.load(file)
process_annotations_to_files(annotation_json, out_path)

