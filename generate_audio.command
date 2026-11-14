#!/bin/bash
# =============================================================================
# 名筆（MEIHITSU）『徒然草』VOICEVOX 音声一括生成ランチャー (Mac用)
# このファイルをダブルクリックするだけで音声生成を実行できます。
# =============================================================================

cd "$(dirname "$0")"

echo "========================================================"
echo " 名筆『徒然草』VOICEVOX 音声生成スクリプトを起動します"
echo "========================================================"
echo ""

# Python3の存在確認
if ! command -v python3 &> /dev/null; then
    echo "【エラー】Python3 が見つかりませんでした。"
    echo "Mac標準のターミナルで 'python3' が実行できるようにインストールしてください。"
    echo ""
    read -p "Enterキーを押して終了します..."
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "実行モードを選択してください:"
    echo "  1: まだ作られていない音声のみ生成（未生成分のみ）"
    echo "  2: すべて上書き再生成（ナレーターや設定を変更したとき）"
    echo "  3: 特定の段だけ作り直す（テキスト修正後のピンポイント上書き）"
    read -p "番号を入力してください (1, 2, 3) [初期値: 1]: " mode
    echo ""
    if [ "$mode" = "2" ]; then
        python3 generate_audio.py --force
    elif [ "$mode" = "3" ]; then
        read -p "作り直したい段番号を入力してください（例: 52）: " sec_num
        echo ""
        python3 generate_audio.py "$sec_num"
    else
        python3 generate_audio.py
    fi
else
    python3 generate_audio.py "$@"
fi

echo ""
read -p "処理が完了しました。Enterキーを押すとこのウィンドウを閉じます..."
