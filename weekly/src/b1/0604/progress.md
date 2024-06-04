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

前回は, ちょっとした UI のプロトタイプを考えて, 技術選定を進めた. 今回はプロジェクトの構築を主に行っていく.

今一度ゴールを再確認 (定期):

> - ★ ユーザーが制作物のライセンスを理解し, 従いやすくする仕組みを作る (行動変容)
>   - 制作物の許諾範囲の簡易一覧を確認できる
>   - ライセンス全文を確認できる
>   - 作品に含まれる素材のライセンスに従うための情報を得られる (クレジット表記のコピー など)
>
> そのために, クリエイターが...
>
> - 自身の作品に対して簡単にライセンスを選択/生成できる
> - 必要に応じて特記事項を追加できる

### 技術選定

<img width="914.25" alt="image.png (125.4 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/06/04/163736/2a1dd44f-786c-4943-99d0-50efc8204119.png">

<p style="font-size: 2rem; font-weight: bold">
→ ...Tauri に決定！
</p

### プロジェクトの構築

- Tauri + Vite + React

ここからはゴールに対してあくまで “手段” のお話になるが, 知見のために, 躓いたところをメモしておく.

### 問題点

よ～し. `src-tauri/src/main.rs` にコマンドを追加してみるよ. これがデモコードか～.

```rs
// ...

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

`invoke_handler` にコマンドを追加することによって, JavaScript (WebView) 側から Rust で記述した関数を呼び出すことができる.

```ts
import { invoke } from "@tauri-apps/api";

const greet = async () => {
  return await invoke("get_app_name");
  //           ^? Promise<any>
};
```

そう. 初期の場合だと, `invoke` した型は, `Promise<any>` になってしまい型が取れない. 悲しい.  
また, `invoke` に渡す引数 (コマンドの名称) も `string` であれば何でも入ってしまうので, そのコマンドが存在するかもわからない. これも悲しい.

<img width="762" alt="image.png (121.9 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/06/04/163736/156dff7f-9c94-4803-9712-8ce1d45f9774.png">

GitHub Issues のコメント [^1] によると, どうやら Rust の RPC があって, rspc というクレートを使えばメインプロセスと WebView プロセスで仲良く通信ができるらしい.

<img width="694.5" alt="image.png (21.2 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/06/04/163736/9804807b-75bd-4aaf-9199-9f3d25adeca7.png">

(脳内変換中...)

```rs
let router = <rspc::Router>::new()
    .query("version", |t| {
      t(|ctx, input: ()| "0.0.1")
    })
    /*
    ->  .query("version", (t) => t((ctx, input: {}) => "0.0.1")
    */
    .mutation("helloWorld", |t| {
      t(|ctx, input: ()| async { "Hello World!" })
    });
    /*
    ->  .mutation("helloWorld", (t) => t(async (ctx, input: {}) => "Hello World!")
    */
```

`|t|` とか `(())` とかは後々慣れるとして, このパッケージを Tauri で使ってみよう.  
Tuari + rspc の記事は, 日本語と英語がヒットしたが, 少しバージョンが古かったので公式ドキュメントを当たってみた:

<img width="1167" alt="image.png (148.9 kB)" src="https://img.esa.io/uploads/production/attachments/13979/2024/06/04/163736/d2fc3107-e848-4687-b6da-5900f279f5fb.png">

なんでや！ `main.rs` がこんな短いわけがないやろ！
すでにあるコードと頑張ってマージしていった.

```log
thread 'main' panicked at 'there is no reactor running, must be called from the context of Tokio runtime'
```

簡単にはいかなかったが, 40 分くらい格闘したらいけた（結局 `Tokio` ってなんだったんだ？）.  
WebView 側の準備 (ESLint + PandaCSS + generouted など) も整ったので, 来週からは本格的な UI の実装に入っていけそうだ.

完成形:

`src-tauri/src/main.rs`

```rs
// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use rspc::Router;

fn router() -> Router<()> {
    <Router>::new()
        .config(rspc::Config::new().export_ts_bindings("../src/types/bindings.d.ts"))
        // ↑ で `/src/types/bindings.d.ts` に次に続く Query などの戻り値の型などが生成される
        .query("version", |t| {
            t(|_ctx, _input: ()| env!("CARGO_PKG_VERSION"))
        })
        .query("hello", |t| t(|_ctx, _input: ()| "Hello, World!"))
        .build()
}

#[tokio::main]
async fn main() {
    let router = router();

    tauri::Builder::default()
        .plugin(rspc_tauri::plugin(router.arced(), |_app_handle| ()))
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

`src/lib/services/rpc.ts`

```ts
import { createClient } from "@rspc/client";
import { TauriTransport } from "@rspc/tauri";
import { type Procedures } from "@/types/bindings";

export const api = createClient<Procedures>({
  transport: new TauriTransport(),
});

// api.query(["version"]).then((res) => console.log(res));
//                      ^? Promise<string> 😊
```

これでずいぶんとコードの見通しが良くなった. これからは, この構成で UI を実装していく.

## 余談

- Typst で情報倫理の中間テストの公式チートシートを作成する → 提出が手書きな故に苦痛なり 🙃

[^1]: <https://github.com/tauri-apps/tauri/issues/1514#issuecomment-1619337304>
