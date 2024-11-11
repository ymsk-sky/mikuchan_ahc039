# mikuchan
AHC039の多角形の形を初音ミクの形で生成するスクリプト

<img src="./vis.png" width=500>

## 画像編集
1. 公式絵を単色化
2. モザイク処理

## script.py
3. 二値化
4. 輪郭抽出
5. 点群リストを調整
    - 同じ点が無いようにする
    - 線が水平か垂直になるようにする

<img src="0_mosiced_img.png" width=200>
<img src="1_bin_img.png" width=200>
<img src="2_res_img.png" width=200>
<img src="3_line_img.png" width=200>

# Library
- OpenCV
- Numpy
