@echo off
chcp 65001 > nul
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

python generate_audio.py %*

echo.
echo 処理が完了しました。
pause
