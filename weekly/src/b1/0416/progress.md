# タイトル

## 出席率

- 3 年セミナー: ?? %

## スケジュール

### 短期的な予定

- [ ] ?/?までに〇〇する
- [ ] ?/?までに〇〇する
- [ ] ?/?までに〇〇する

### 長期的な予定

来月までに〇〇する？
今季までに〇〇する？

## 進捗報告

とりあえずセンシングの基礎を固めるために, スマホで計測したデータを Python を使ってグラフにした.
[phyphox ↗](https://phyphox.org/) というアプリで計測したデータを CSV ファイルにエクスポートして, それを pandas で読み込んでグラフにした.

X, Y, Z 軸は以下のようになっているらしい:  
<img width="417" alt="image.png (31.8 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/9b686bb2-de2e-49a3-8f91-3a07b1837d5d.png">

```py
import pandas as pd
from whitecanvas import new_canvas

data = pd.read_csv("./src/assets/data.csv")

x = data["x"].to_numpy()
y = data["y"].to_numpy()
z = data["z"].to_numpy()
t = data["t"].to_numpy()

canvas = new_canvas("pyqtgraph")
canvas.add_line(t, x, name="X-axis")
canvas.add_line(t, y, name="Y-axis")
canvas.add_line(t, z, name="Z-axis")
canvas.add_legend(location="right_side_top")
canvas.show(block=True)
```

- 実験 1
  スマホを 2 m ほどの高さから自由落下させた.  
  <img width="269.25" alt="image.png (16.6 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/eb29441b-d6d4-416f-ab8f-570633cfd6fa.png">

  - 図 1: X, Y, Z 軸の加速度の変化  
    <img width="NaN" alt="X, Y, Z 軸の加速度の変化" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/98c2a06b-5143-4651-af66-8e79785eaaa9.svg">

    考察:

    - 1.11-1.6 s 付近で自由落下していることがわかる.
    - それ以降は布団でバウンドしている感じかも.

    → その区間だけ取り出してみる

    ```diff
    + t_start = 1.11
    + t_end = 1.6
    + data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
    ```

  - 図 2: スパイクを除いた自由落下時の X, Y, Z 軸の加速度の変化  
    <img width="NaN" alt="スパイクを除いた自由落下時の X, Y, Z 軸の加速度の変化" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/4e1159dc-7fcf-43d1-97bd-4b076509abfc.svg">
    考察:

    - 最初は人間のノイズ()
    - だんだん加速度が増加していることがわかる

    → 加速度を 2 回積分したら変位になるので, それをプロットしてみる
    → どうやら積分の代わりに累積和を使うらしい (今度よく調べる)

    ```diff
    + x = x.cumsum().cumsum()
    + y = y.cumsum().cumsum()
    + z = z.cumsum().cumsum()
    ```

  - 図 3: 図 2 での加速度の累積和を取った X, Y, Z 軸の加速度の変化  
    <img width="NaN" alt="図 2 での加速度の累積和を取った X, Y, Z 軸の加速度の変化" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/d3b6c54d-ecd8-4247-be2a-fbcd5d483ec4.svg">
    考察:
    - Z 軸 (ベッドからスマホまでの高さ) が自由落下っぽくなっている

- 実験 2
  スマホを ~~感覚で~~ 斜方投射する.  
  <img width="316.5" alt="image.png (21.4 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/0fa15f53-192d-4b8e-ad26-4d6dd2bcdec1.png">

  - 図 1: X, Y, Z 軸の加速度の変化  
    <img width="NaN" alt="4.svg (141.2 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/5ff32c89-b763-48fa-a81b-8c0c59d772ec.svg">

    考察:

    - 1.11-1.6 s 付近で自由落下していることがわかる.
    - それ以降は布団でバウンドしている感じかも.

    → その区間だけ取り出してみる

    ```diff
    + t_start = 1.11
    + t_end = 1.6
    + data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
    ```

  - 図 2: スパイクを除いた自由落下時の X, Y, Z 軸の加速度の変化  
    <img width="NaN" alt="5.svg (52.7 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/0a99dbd9-1035-4aba-83d2-52ffd5f7a81e.svg">
    考察:

    - 最初は人間のノイズ()
    - だんだん加速度が増加していることがわかる

    → 加速度を 2 回積分したら変位になるので, それをプロットしてみる
    → どうやら積分の代わりに累積和を使うらしい (今度よく調べる)

    ```diff
    + x = x.cumsum().cumsum()
    + y = y.cumsum().cumsum()
    + z = z.cumsum().cumsum()
    ```

  - 図 3: 図 2 での加速度の累積和を取った X, Y, Z 軸の加速度の変化  
    <img width="NaN" alt="6.svg (53.5 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/92ef4ad1-78a5-424c-836b-cbe3c40f1729.svg">
    考察:
    - Z 軸 (ベッドからスマホまでの高さ) が自由落下っぽくなっている

## 進路関係

## Appendix

使用したコードは以下の手順で実行できます:

```sh
git clone https://github.com/wappon28dev/kajilab
cd kajilab/weekly
poetry install --with b1-0423
poetry run python ./src/b1/0423/main.py
```
