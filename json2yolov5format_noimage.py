import os
import math
import json 

json_file_path ="YOURFILE.json"
out_path = "YOUR_OUTPUT_PATH"
false = "False"
null = "null"

#中身を変更してください。
class_mapping = {
    "abdomen": 0,
    "humerus": 1,
    "lung": 2,
    "mediastinum": 3,
    "spine": 4
}

# 四隅の座標を回転する関数
def rotate_point(x_center, y_center, theta, x, y):
    x_rotated = x_center + (x - x_center) * math.cos(theta) - (y - y_center) * math.sin(theta)
    y_rotated = y_center + (x - x_center) * math.sin(theta) + (y - y_center) * math.cos(theta)
    return x_rotated, y_rotated

# アノテーションデータを処理してファイルに書き込む関数
def process_annotations_to_files(annotation_json, out_path):
    for annotation in annotation_json:
        # ファイル名の抽出
        image_path = annotation["data"]["image"]
        file_name = image_path.split('/')[-1].replace('.jpg', '') + '.txt'         
        full_file_path = os.path.join(out_path, file_name)

        # ファイルを開く
        with open(full_file_path, 'w') as file:
            for ann in annotation['annotations']:
                for result in ann['result']:
                    # 基本パラメータの計算
                    original_width = result['original_width']
                    original_height = result['original_height']
                    value = result['value']
                    label = value['rectanglelabels'][0]
                    label_class = class_mapping[value['rectanglelabels'][0]]

                    # 中心座標、幅、高さ、回転の計算
                    x_center = value['x'] / 100 * original_width
                    y_center = value['y'] / 100 * original_height
                    width = value['width'] / 100 * original_width
                    height = value['height'] / 100 * original_height
                    rotation_radians = math.radians(value['rotation'])

                    # 四隅の座標（回転前）
                    x_tl = x_center
                    y_tl = y_center
                    x_tr = x_center + width
                    y_tr = y_center
                    x_br = x_center + width
                    y_br = y_center + height
                    x_bl = x_center
                    y_bl = y_center + height

                    # 四隅の座標を回転
                    x1, y1 = rotate_point(x_center, y_center, rotation_radians, x_tl, y_tl)
                    x2, y2 = rotate_point(x_center, y_center, rotation_radians, x_tr, y_tr)
                    x3, y3 = rotate_point(x_center, y_center, rotation_radians, x_br, y_br)
                    x4, y4 = rotate_point(x_center, y_center, rotation_radians, x_bl, y_bl)

                    # ファイルに書き込み
                    file.write(f"{x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} {label} 0\n")

# テスト実行（実際のデータで実行する場合はannotation_jsonにデータを挿入する）
# JSONファイルを開いて内容を読み込む
with open(json_file_path, 'r') as file:
    annotation_json = json.load(file)
process_annotations_to_files(annotation_json, out_path)

