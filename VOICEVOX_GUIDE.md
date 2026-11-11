# VOICEVOX 音声一括生成ガイド（初心者向け手順書）

本ガイドは、ご自身のパソコン上でVOICEVOXを使って『徒然草』の音声（原文朗読・ざっくり訳朗読）を一括生成するための手順書です。

---

## 1. 準備（初回のみ）

### ① VOICEVOX のインストールと起動
1. **[VOICEVOX 公式サイト](https://voicevox.hiroshiba.jp/)** から、お使いのOS（Mac または Windows）に合わせたインストーラーをダウンロードします。
2. インストール後、**「VOICEVOX」アプリを普通に起動**します。
   * ウィンドウが表示されていれば、バックグラウンドでローカル音声エンジン（`http://127.0.0.1:50021`）が自動的に待機状態になります。

### ② Python の確認
* **Mac**: 最初から Python3 が入っています（特別な操作は不要です）。
* **Windows**: 入っていない場合は [python.org](https://www.python.org/) からインストールしてください（インストール画面で **「Add Python to PATH」に必ずチェック** を入れてください）。

---

## 2. 音声キャラクター（話者ID）の変更方法

生成するキャラクターを変更したい場合は、[`generate_audio.py`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/generate_audio.py) をメモ帳やテキストエディタで開き、29行目あたりの **`SPEAKER_ID = 3`** の数字を書き換えるだけです。

### 主な話者ID一覧
| 話者ID | キャラクター名 | スタイル | 声の印象・おすすめ度 |
| :---: | :--- | :--- | :--- |
| **3** | **ずんだもん** | ノーマル | 初期設定。明るく聞き取りやすい。 |
| **2** | **四国めたん** | ノーマル | 落ち着いた上品な語り。古典の朗読によく合います。 |
| **13** | **青山龍星** | ノーマル | 重厚な男声・僧侶風。徒然草の世界観に抜群に合います。 |
| **9** | **波音リツ** | ノーマル | クールで明瞭な語り口。 |
| **14** | **冥鳴ひまり** | ノーマル | 柔らかく親しみやすいトーン。 |
| **8** | **春日部つむぎ** | ノーマル | 明るい埼玉ギャル風・現代的。 |

> **ヒント**: 全キャラクターの話者IDを確認したい場合は、VOICEVOXを起動した状態でブラウザで `http://127.0.0.1:50021/speakers` を開くと一覧が表示されます。

---

## 3. 音声の生成実行（ダブルクリックするだけ）

VOICEVOXが起動している状態で、以下のファイルをダブルクリックします：

* **Macをお使いの場合**:  
  [`generate_audio.command`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/generate_audio.command) をダブルクリックします。  
  （初回のみ「開発元が未確認」と出る場合は、右クリック ➔「開く」を選択してください）
* **Windowsをお使いの場合**:  
  [`generate_audio.bat`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/generate_audio.bat) をダブルクリックします。

### 実行の流れ
1. VOICEVOXへの接続を自動チェックします。
2. 序段から第155段まで、全10段の「原文（発音表記）」と「ざっくり訳」を自動生成します（計20ファイル）。
3. 生成された音声は [`audio/tsurezure/`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/audio/tsurezure/) フォルダに保存されます。
4. 各音声の再生時間（duration）が自動計測され、[`data/tsurezuregusa.js`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/data/tsurezuregusa.js) に自動反映されます。
5. 「全処理完了」と表示されたら、Enterキーを押して画面を閉じます。

---

## 4. 便利なオプション操作

### すでに作った音声を上書き再生成したい場合
キャラクターや速度を変更して最初からすべて作り直したい場合は、ターミナルで以下を実行します：
```bash
python3 generate_audio.py --force
```

### 特定の段だけ作り直したい場合
例えば第52段（仁和寺）だけを作り直したい場合は、段番号を指定します：
```bash
python3 generate_audio.py 52
```

---

## 5. ブラウザでの確認
音声生成が完了したら、[`index.html`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/index.html) をダブルクリックしてブラウザで開くだけで、VOICEVOXの音声で「原文 ➔ 現代語訳」の連続再生が楽しめます！
