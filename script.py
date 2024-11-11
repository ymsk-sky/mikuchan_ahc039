import cv2
import numpy as np


def imshow(img: np.ndarray, name: str = "img") -> None:
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> list:
    # グレースケールで読み込み
    img = cv2.imread("./mosiced_miku.png", cv2.IMREAD_GRAYSCALE)
    # 二値化
    _, bin_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    imshow(bin_img)
    cv2.imwrite("1_bin_img.png", bin_img)

    # 輪郭抽出: 外枠のみ
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    res_img = np.zeros_like(img)
    cv2.drawContours(res_img, contours, -1, 255, -1)
    imshow(res_img)
    cv2.imwrite("2_res_img.png", res_img)

    # 点群リスト作成
    points = contours[0].tolist()
    res = [points[0][0]]
    for p in points:
        _x, _y = res[-1]
        x, y = p[0]
        dx = abs(x - _x)
        dy = abs(y - _y)
        if dx < 3 and dy < 3:
            # 前の点に近すぎる場合は不採用
            continue
        # 前の点と差が小さいほうを合わせて垂直/平行にする
        if dx < dy:
            x = _x
        else:
            y = _y
        res.append([x, y])

    p_img = np.zeros((*img.shape, 3), dtype=np.uint8)
    used = set()  # 同じ点がないかチェック(提出用)
    for i, (r1, r2) in enumerate(zip(res, res[1:] + [res[0]])):
        cv2.line(p_img, r1, r2, (255, 255, 255), 1)
        if tuple(r1) in used:
            print(i, r1, r2)
            cv2.circle(p_img, r1, 2, (0, 255, 0), -1)
            cv2.circle(p_img, r2, 2, (255, 0, 0), -1)
        used.add(tuple(r1))

    imshow(p_img)
    cv2.imwrite("3_line_img.png", p_img)
    return res


def update(res: list) -> list:
    left = top = float("inf")
    right = bottom = 0
    for x, y in res:
        left = min(left, x)
        right = max(right, x)
        top = min(top, y)
        bottom = max(bottom, y)
    # スケーリング
    rate = 35000 // min(right - left, bottom - top)
    res = [[rate*x, rate*y] for x, y in res]
    # 平行移動
    res = [[x + 10000, 100_000 - y - 20000] for x, y in res]

    # 同じ点が無いかチェック
    s = set()
    for x, y in res:
        if (x, y) in s:
            print("NO!!!!")
        s.add((x, y))
    return res


if __name__ == "__main__":
    res = main()
    res = update(res)
    # 線の長さの合計は検査サイトで手動チェック
    print(len(res))
    for x, y in res:
        print(x, y)
