@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
rem =============================================================================
rem 名筆（MEIHITSU）『徒然草』VOICEVOX 音声一括生成ランチャー (Windows用)
rem このファイルをダブルクリックするだけで音声生成を実行できます。
rem =============================================================================

cd /d "%~dp0"

echo ========================================================
echo  名筆『徒然草』VOICEVOX 音声生成スクリプトを起動します
echo ========================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 【エラー】Python が見つかりませんでした。
    echo Python公式サイト（https://www.python.org/）からPythonをインストールし、
    echo インストール時に「Add Python to PATH」にチェックを入れてください。
    echo.
    pause
    exit /b 1
)

if "%~1"=="" (
    echo 実行モードを選択してください:
    echo   1: まだ作られていない音声のみ生成（未生成分のみ）
    echo   2: すべて上書き再生成（ナレーターや設定を変更したとき）
    echo   3: 特定の段だけ作り直す（テキスト修正後のピンポイント上書き）
    set /p mode="番号を入力してください (1, 2, 3) [初期値: 1]: "
    echo.
    if "%mode%"=="2" (
        python generate_audio.py --force
    ) else if "%mode%"=="3" (
        set /p sec_num="作り直したい段番号を入力してください（例: 52）: "
        echo.
        python generate_audio.py !sec_num!
    ) else (
        python generate_audio.py
    )
) else (
    python generate_audio.py %*
)

echo.
echo 処理が完了しました。
pause
