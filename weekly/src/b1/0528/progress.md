# タイトル

## 出席率

- 3 年セミナー：?? %

## スケジュール

### 短期的な予定

- [ ] ?/?までに〇〇する
- [ ] ?/?までに〇〇する
- [ ] ?/?までに〇〇する

### 長期的な予定

- 8/15 ソフトウェア完成
- 8/25 作品紹介動画の制作完了, ProtoPedia 執筆完了
- 8/31 U-22 プログラミングコンテスト作品提出

## 進捗報告

前回は機能別に仕様を整理し,

- Viewer
- Generator
- Manager (Viewer + Generator)

の 3 つの機能の実装を考えた. 今回は, ちょっとした UI のプロトタイプを考えて, 技術選定も含めて進めていく.

### ゴールと機能一覧

今一度ゴールを再確認:

> - ★ ユーザーが制作物のライセンスを理解し, 従いやすくする仕組みを作る (行動変容)
>   - 制作物の許諾範囲の簡易一覧を確認できる
>   - ライセンス全文を確認できる
>   - 作品に含まれる素材のライセンスに従うための情報を得られる (クレジット表記のコピー など)
>
> そのために, クリエイターが...
>
> - 自身の作品に対して簡単にライセンスを選択/生成できる
> - 必要に応じて特記事項を追加できる

そして, ソフトウェアが介入する機能も再確認:
<img width="1127.25" alt="image.png (171.7 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/05/21/163736/6bf491ed-e3d3-4b70-adb7-55f8ffe64307.png">

### UI のプロトタイプ

- Viewer
  <img width="1091.25" alt="image.png (184.8 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/05/28/163736/fd5744cb-de10-463b-93f4-2de4c738e6b8.png">
- Generator
  <img width="1144.5" alt="image.png (96.3 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/05/28/163736/05987979-2b8f-4d39-be83-cf213b9ad2bb.png">  
  <img width="747" alt="image.png (84.5 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/05/28/163736/072c5701-809c-4f93-8ece-c53b79357ccc.png">  
  <img width="765.75" alt="image.png (149.1 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/05/28/163736/0a89d481-cc0f-43b3-bd1c-1b9968925905.png">

- Manager
  Viewer と Generator ができあがってから考える

### 技術選定

<img width="919.5" alt="image.png (122.4 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/05/28/163736/e4daccc3-76bd-41ba-98be-8d19d1ec4f12.png">
