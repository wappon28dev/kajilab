# タイトル

## 出席率

- 3 年セミナー：?? %

## スケジュール

### 短期的な予定

- [ ] ?/?までに〇〇する
- [ ] ?/?までに〇〇する
- [ ] ?/?までに〇〇する

### 長期的な予定

来月までに〇〇する？
今季までに〇〇する？

## 進捗報告

### とりあえず前回の疑問点を晴らす

1. 変位を求めるために積分の代わりに累積和を使う理由
1. グラフの単位がおかしい
1. 加速度を単純に積分しても正しい行動が取れないらしい
1. 動物行動の事例をまとめる

皆さん既にご存知の箇所が多いかもですが, 確認ということで間違いあればぜひご指摘ください……

### 累積和

累積和とは, 配列の任意の空間の総和を求めるためのアルゴリズムのこと[^1].  
次の図[^2] のように, ある区間の総和を求める際に, その区間の始点から終点までの値を足し合わせることで求めることができる.
(AtCoder の記事しか出てこない)

<img src="https://prtechblogfd-crhzb5g6hkhqafdm.z01.azurefd.net/drupalimages/%5Bdate%3Acustom%3AY%5D/%5Bdate%3Acustom%3Am%5D/%5Bdate%3Acustom%3Ad%5D/articleimages/2023-12-14-can-you-solve-this-a-002.gif" alt="累積和の説明図" height="auto" width="700px" />

どこかで見たことあるような……　長い足し算のときに知らず知らず使っていたよ (驚愕).
直近だと, 論理回路の IRAT の進数変換の問題で $2^0 + 2^2 + 2^4 + 2^8 + \cdots$ とかの下に書いていたよ:
<img width="1362" alt="知らず知らず使われる累積和" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/ea0f1281-1a32-48ec-9041-fb9f367051a9.png" />

前回は加速度を積分して変位を求めるときに, 累積和を 2 回取っていたが, このままでは値が大きくなりすぎてしまう. 加速度データの累積和に時間間隔を掛けてあげることで正しい値を得ることができるはず.

時間間隔は, その定義より, サンプリングレートから求めることができるので, まずはサンプリングレートを求める.

### サンプリングレートを測定する

前回取れたデータを確認:

```csv
"t","x","y","z","a"
5.989802400E-2,-2.066427469E-1,1.766612828E-1,-1.535520554E-1,3.122317527E-1
6.481031600E-2,-2.062166929E-1,1.877931952E-1,-3.107919693E-1,4.175922135E-1
6.973083700E-2,-2.433449030E-1,1.268998086E-1,-3.566465378E-1,4.500189509E-1
︙
```

そもそも数値に付いている `/E[+-]\d+/` とは？
$e$ ってネイピア数じゃないの？　 → 指数 (**e**xp) の e らしい (無知) <img src="https://img.esa.io/uploads/production/attachments/13979/2024/04/21/163736/b737c1ff-5ca8-46ab-8284-34b1cdbc7978.png" height="30px" width="30px" alt="あたまのわるいひと" />

> `e` は 10 のべき乗を表します。
> 大きい数字は `1e3` のように `e` を使って表すことがあります。  
> 0 に近い数字も `1e-3` のように `e` を使って表すことがあります。
> `1e3` は $10^3$ で 1000 で、`1e-3` は $10^{-3}$ で 0.001 です。
>
> <p style="text-align: right;"> — <a href="https://mathwords.net/ehyouki">1e5、1e-6、1E+9などの数値の意味と注意点 - 具体例で学ぶ数学 ↗</a> より</p>

ほう……　たしかに電卓のオーバー/アンダーフローで見たことあるかもしれない.

<video controls width="700px" alt="電卓でのオーバーフロー" src="https://esa-storage-tokyo.s3-ap-northeast-1.amazonaws.com/uploads/production/attachments/13979/2024/04/22/163736/1a786a5e-17b4-4467-bf7c-f759fd9a0aee.mp4"></video>

phyphox で取れるデータの $t$ の単位は秒 (s) なので,

$$
\text{サンプリングレート} = \frac{\text{サンプル数}}{\text{最後の時間} - \text{最初の時間}}
$$

で求められる.

求めるサンプリングレートを $f$ Hz, サンプル数を $n$, 総時間を $t$ s としてサンプリングレートを Python で算出してみた:

```py
def calc_freq(data: DataFrame) -> float:
    t = data["t"].to_numpy()
    total_t: float = t[-1] - t[0]
    n: int = len(t)
    f: float = n / total_t

    print(f"{total_t=}, {n=}, {f=} Hz")
    # stdout -> total_t=4.937588750000001, n=990, f=200.50272514088985 Hz
    return f

# ...
data = read_csv(assets_dir_0416 / "1.csv")
f = calc_freq(data)
```

ｲｲﾈ!　約 200.5 Hz でサンプリングされていることが分かった.
加速度データの累積和を算出するときにこいつの逆数 (時間間隔 $dt$ s) を掛けてあげる.

```diff
# ...
+ dt = 1 / f
+ dx = (x.cumsum() * dt).cumsum() * dt
+ dy = (y.cumsum() * dt).cumsum() * dt
+ dz = (z.cumsum() * dt).cumsum() * dt

show_graph(t, dx, dy, dz)
```

グラフができたので, 前回の単位バグりまくりのグラフと比較してみた.

- 自由落下

  (左: 累積和を用いたもの　右: 適切な時間間隔を掛けた累積和を用いたもの)

  <img width="400px" alt="累積和を使った X, Y, Z 軸の加速度の変化 (自由落下)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/d3b6c54d-ecd8-4247-be2a-fbcd5d483ec4.svg" />
  <img width="400px" alt="累積和に適切な時間間隔を掛けた X, Y, Z 軸の加速度の変化 (自由落下)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/a69c0f55-f282-48e7-9d18-1ba4753c95ed.svg" />

- 斜方投射

  (左: 累積和を用いたもの　右: 適切な時間間隔を掛けた累積和を用いたもの)

  <img width="400px" alt="累積和を使った X, Y, Z 軸の加速度の変化 (斜方投射)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/16/163736/92ef4ad1-78a5-424c-836b-cbe3c40f1729.svg" />
  <img width="400px" alt="累積和に適切な時間間隔を掛けた X, Y, Z 軸の加速度の変化 (斜方投射)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/201939f7-eca6-4e5c-9183-4926a75b89a5.svg" />

どちらもグラフの形こそ変わっていないが, Z 軸の値がそれぞれ −35000 m → −1.0 m, 40000 m → 1.0 m に適切に変動していることが分かる.

## 台形積分もやってみる

どうやら次の資料[^3] によると, 台形積分を使うのも一般的らしい. (先にこの資料を見つけ出す必要があったな.)

<img width="700px" alt="image.png (191.1 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/94980613-e98e-4b85-a745-0f903d21e984.png">

算出に必要な時間間隔 $dt$ は, 先ほど求めたサンプリングレートを使う.  
台形積分を公式通りに実装してみた:

```py
float1DArr = ndarray[float, dtype[float64]]

def integrate(
    data: float1DArr,
    dt: float,
) -> float1DArr:
    result = zeros_like(data)
    for i in range(1, len(data)):
        result[i] = result[i - 1] + (data[i] + data[i - 1]) * dt / 2
    return result

# ...
dt = 1 / f
dx = integrate(integrate(x, dt), dt)
dy = integrate(integrate(y, dt), dt)
dz = integrate(integrate(z, dt), dt)

show_graph(t, dx, dy, dz)
```

同じような形のグラフができたので, 累積和で求めたものと比較してみた:

- 自由落下

  (左: 適切な時間間隔を掛けた累積和を用いたもの　右: 台形積分を用いたもの)

  <img width="400px" alt="累積和に適切な時間間隔を掛けた X, Y, Z 軸の加速度の変化 (自由落下)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/a69c0f55-f282-48e7-9d18-1ba4753c95ed.svg" />
  <img width="400px" alt="台形積分を用いた X, Y, Z 軸の加速度の変化 (自由落下)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/34c3b347-8348-4b47-b760-5d958ff0967b.svg" />

- 斜方投射

  (左: 適切な時間間隔を掛けた累積和を用いたもの　右: 台形積分を用いたもの)

  <img width="400px" alt="累積和に適切な時間間隔を掛けた X, Y, Z 軸の加速度の変化 (斜方投射)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/201939f7-eca6-4e5c-9183-4926a75b89a5.svg" />
  <img width="400px" alt="台形積分を用いた X, Y, Z 軸の加速度の変化 (斜方投射)" src="https://img.esa.io/uploads/production/attachments/13979/2024/04/22/163736/e4d5a652-4834-4260-b393-e4c21f59225c.svg" />

適切な時間間隔を掛けた累積和を用いたものでも, 台形積分を用いたものでも, 単位と数値がぴったりになることが分かった！　スッキリ！

ほかにも, 計測時にスマホが完全に水平になっているとは限らない.
このサイト[^4] によると, その分の傾きを考慮して計算をしたり, ほかの軸を考慮して補正値を求めたりが必要になることもあるので, 今後の計測.
今回は適当にスマホを感覚で適当に投げたので, このデータの精度について確かめられないが……

## まとめ

前回の疑問点を晴らすためにかなり時間を要した.　楽しいけど苦しい.　来週以降は……

- 動物センシングの事例を調査
  - どのターゲットにどんな情報を見せるかを決める (or その事例)
  - 自身がやってきた動物行動のモニタリングとダイジェスト化とどう統合するか考える
- U-22 プログラミングコンテストに向けて, 少し面白い構想を思いついたのでそれを進捗として進めるかもしれない
  - 梶研内での個人活動かシス研内の個人活動とするかはまだ決める
  - 後日, 梶先生と相談

<!--
- ライセンスツリー
  → ハッシュ or license.yaml でライセンス表記を生成
  → プログラミング界隈のライセンスの明文化は良いこと
  → VRChat アバターやキャラクター, 絵師さんなど色んな界隈のライセンス表記にはブレがある → ソフトウェアとの兼ね合いが難しいことも
   - AI 学習問題やキャラクターイメージの毀損などを防ぐために GUI ⇔ ライセンス文 を作る
   - それ用の言語を作っても面白いかも
   - ライセンスツリーを作って dependency を測定 → 制作者への感謝の気持ち
   - 制作者が GUI でライセンス文を生成 → ライセンス文のハッシュが一致したら簡易版を表示できる
   - ライセンス文–YAML–制作物–ユーザー認証で署名 → ブロックチェーンにしたら面白いかも
   - リポジトリは Google Drive や One Drive など一元化をせず分散型で管理
-->

## Appendix

使用したコードは以下の手順で実行できます:

```sh
git clone https://github.com/wappon28dev/kajilab --depth 1
cd ./kajilab/weekly
poetry install --with b1-0423
poetry run python ./src/b1/0423/main.py
```

[^1]: [アルゴリズム（Ruby）累積和の解説 - じゃいごテック ↗](https://jaigotec.com/algorithm_prefix_sum/#i)
[^2]: [これ、解けますか？【累積和】- tech blog ↗](https://tech-blog.cloud-config.jp/2023-12-14-can-you-solve-this-a#%E7%B4%AF%E7%A9%8D%E5%92%8C%E3%81%A3%E3%81%A6%E3%81%AA%E3%81%AB)
[^3]: [物理教育のための携帯機器の加速度センサーを用いた運動の測定実験 - KIT Progress ↗](https://kitir.kanazawa-it.ac.jp/infolib/cont/01/G0000002repository/000/000/000000240.pdf)
[^4]: [本当に加速度を計測できているのか？ - ツクツクボウシの自由研究 ↗︎](https://www.tsukutsuku-lab.com/%E3%82%B9%E3%83%9E%E3%83%9B%E5%86%85%E8%94%B5%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E3%81%A7%E5%AE%9F%E9%A8%93/%E6%9C%AC%E5%BD%93%E3%81%AB%E5%8A%A0%E9%80%9F%E5%BA%A6%E3%82%92%E8%A8%88%E6%B8%AC%E3%81%A7%E3%81%8D%E3%81%A6%E3%81%84%E3%82%8B%E3%81%AE%E3%81%8B/)
