#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
名筆（MEIHITSU）『徒然草』VOICEVOX 音声一括生成スクリプト
=============================================================================
このスクリプトは、ローカルPCで起動しているVOICEVOXエンジンと通信し、
『徒然草』の「原文（発音表記）」と「ざっくり訳」の2種類の音声ファイルを
自動生成して保存します。

【動作要件】
- Python 3.7 以上（標準ライブラリのみで動作、追加pipインストール不要）
- VOICEVOX（アプリを起動しておくだけでOK）
- ffmpeg（任意：PCに入っていればMP3、なければWAVで出力）
=============================================================================
"""

import os
import sys
import json
import time
import wave
import io
import subprocess
import urllib.request
import urllib.parse
import urllib.error

# =============================================================================
# 設定パラメータ（ここをお好みに合わせて変更できます）
# =============================================================================

# VOICEVOXエンジンのURL（通常はデフォルトのままでOK）
VOICEVOX_URL = "http://127.0.0.1:50021"

# 話者ID（キャラクターとスタイルの指定）
# 例: 3=ずんだもん(ノーマル), 2=四国めたん(ノーマル), 13=青山龍星(ノーマル), 9=波音リツ(ノーマル)
# ※話者ID一覧の調べ方は VOICEVOX_GUIDE.md を参照
SPEAKER_ID = 3

# 話す速度
SPEED_ORIGINAL = 0.90      # 原文朗読の速度（古文の格調と聞き取りやすさのため少しゆったり）
SPEED_TRANSLATION = 1.00   # ざっくり訳の速度（自然な現代語の会話ペース）

# 音声の間（秒）
PAUSE_BETWEEN_LINES = 0.35 # 行と行の間の無音時間（秒）
PRE_SILENCE = 0.20         # 発声開始前の無音時間（秒）
POST_SILENCE = 0.30        # 発声終了後の無音時間（秒）

# 出力先ディレクトリ・データファイル
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio", "tsurezure")
DATA_FILE = os.path.join(BASE_DIR, "data", "tsurezuregusa.js")

# MP3ビットレート（ffmpeg使用時）
MP3_BITRATE = "96k"

# =============================================================================
# ユーティリティ関数
# =============================================================================

def check_voicevox_running():
    """VOICEVOXエンジンが起動しているか確認する"""
    url = f"{VOICEVOX_URL}/version"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            version = resp.read().decode("utf-8").strip().strip('"')
            return True, version
    except Exception as e:
        return False, str(e)


def check_ffmpeg_available():
    """ffmpegコマンドが使えるか確認する"""
    try:
        res = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0
    except Exception:
        return False


def create_audio_query(text, speaker_id, speed_scale):
    """VOICEVOXにテキストを送って音声合成クエリを取得する"""
    params = urllib.parse.urlencode({
        "text": text,
        "speaker": speaker_id
    })
    url = f"{VOICEVOX_URL}/audio_query?{params}"
    req = urllib.request.Request(url, method="POST", headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        query_data = json.loads(resp.read().decode("utf-8"))
    
    # 速度や無音の設定を反映
    query_data["speedScale"] = speed_scale
    query_data["prePhonemeLength"] = PRE_SILENCE
    query_data["postPhonemeLength"] = POST_SILENCE
    
    return query_data


def synthesize_audio(query_data, speaker_id):
    """クエリデータをもとにWAVバイナリ音声を合成する"""
    params = urllib.parse.urlencode({"speaker": speaker_id})
    url = f"{VOICEVOX_URL}/synthesis?{params}"
    data_bytes = json.dumps(query_data).encode("utf-8")
    
    req = urllib.request.Request(url, data=data_bytes, method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def make_silence_wav(duration_sec, framerate=24000, sampwidth=2, nchannels=1):
    """指定秒数の無音PCMバイト列を生成する"""
    num_frames = int(duration_sec * framerate)
    return b"\x00" * (num_frames * sampwidth * nchannels)


def concatenate_wav_data(wav_data_list, pause_sec=0.35):
    """複数のWAVバイナリを無音を挟んで結合する"""
    if not wav_data_list:
        return None
    if len(wav_data_list) == 1 and pause_sec == 0:
        return wav_data_list[0]
    
    frames_list = []
    framerate = 24000
    sampwidth = 2
    nchannels = 1
    
    for idx, wdata in enumerate(wav_data_list):
        with io.BytesIO(wdata) as bio:
            with wave.open(bio, "rb") as wf:
                framerate = wf.getframerate()
                sampwidth = wf.getsampwidth()
                nchannels = wf.getnchannels()
                frames = wf.readframes(wf.getnframes())
                frames_list.append(frames)
                if idx < len(wav_data_list) - 1 and pause_sec > 0:
                    frames_list.append(make_silence_wav(pause_sec, framerate, sampwidth, nchannels))
    
    out_bio = io.BytesIO()
    with wave.open(out_bio, "wb") as out_wf:
        out_wf.setnchannels(nchannels)
        out_wf.setsampwidth(sampwidth)
        out_wf.setframerate(framerate)
        for chunk in frames_list:
            out_wf.writeframes(chunk)
    
    return out_bio.getvalue()


def get_wav_duration_seconds(wav_bytes):
    """WAVバイナリから正確な再生秒数を取得する"""
    with io.BytesIO(wav_bytes) as bio:
        with wave.open(bio, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)


def format_duration(seconds):
    """秒数を mm:ss 形式の文字列にフォーマットする"""
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m}:{s:02d}"


def convert_wav_to_mp3(wav_path, mp3_path):
    """ffmpegを使ってWAVを軽量なMP3に変換する"""
    cmd = [
        "ffmpeg", "-y",
        "-i", wav_path,
        "-ac", "1",
        "-b:a", MP3_BITRATE,
        mp3_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode == 0


def load_dataset():
    """data/tsurezuregusa.js を読み込む"""
    if not os.path.exists(DATA_FILE):
        print(f"[エラー] データファイルが見つかりません: {DATA_FILE}")
        sys.exit(1)
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    marker = "window.TSUREZUREGUSA_DATA ="
    if marker not in content:
        print("[エラー] データファイル内の 'window.TSUREZUREGUSA_DATA =' が見つかりません。")
        sys.exit(1)
    
    json_part = content.split(marker, 1)[1].strip().rstrip(";")
    data = json.loads(json_part)
    return data


def save_dataset(data):
    """data/tsurezuregusa.js に再生時間等を書き戻す"""
    header = (
        "// =============================================================================\n"
        "// 名筆（MEIHITSU）『徒然草』フェーズ1 試作10段データ\n"
        "// 原文：パブリックドメイン（校註日本文学大系・国文大観等照合）\n"
        "// 現代語訳・発音表記：名筆オリジナル\n"
        "// =============================================================================\n\n"
    )
    js_content = header + "window.TSUREZUREGUSA_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)


# =============================================================================
# メイン処理
# =============================================================================

def main():
    print("=" * 70)
    print("  名筆（MEIHITSU）『徒然草』VOICEVOX 音声一括生成ツール")
    print("=" * 70)
    
    # 1. 接続確認
    print("\n[1/4] VOICEVOXエンジンへの接続を確認しています...")
    ok, ver = check_voicevox_running()
    if not ok:
        print("\n" + "!" * 70)
        print("【エラー】VOICEVOXエンジンに接続できませんでした。")
        print("  確認先: " + VOICEVOX_URL)
        print("\n【解決手順】")
        print("  1. パソコンで「VOICEVOX」アプリを起動してください。")
        print("  2. アプリのウィンドウが表示されたら、バックグラウンドでエンジンが自動待機します。")
        print("  3. 起動後、もう一度このスクリプトを実行してください。")
        print("!" * 70 + "\n")
        sys.exit(1)
    
    print(f"  -> 接続成功！ VOICEVOX バージョン: {ver}")
    print(f"  -> 使用話者ID: {SPEAKER_ID}")
    
    # 2. ffmpeg確認
    has_ffmpeg = check_ffmpeg_available()
    if has_ffmpeg:
        print("  -> ffmpeg を検出しました（MP3形式 96kbps で出力します）")
    else:
        print("  -> ffmpeg は検出されませんでした（高音質WAV形式でそのまま出力します）")
        print("     ※ブラウザ再生はWAV形式でも完全に動作します。")
    
    # 3. 引数の解析（特定段の指定や強制再生成フラグ）
    args = sys.argv[1:]
    force_all = ("--force" in args) or ("-f" in args)
    specified_secs = []
    for a in args:
        if a.isdigit():
            specified_secs.append(int(a))
    
    os.makedirs(AUDIO_DIR, exist_ok=True)
    dataset = load_dataset()
    works = dataset.get("works", [])
    
    target_works = works
    if specified_secs:
        target_works = [w for w in works if w.get("no") in specified_secs]
        print(f"\n[2/4] 指定された段（{len(target_works)}段）のみ生成します: {specified_secs}")
    else:
        print(f"\n[2/4] 全{len(works)}段を対象として処理を開始します。")
    
    # 4. 音声生成ループ
    print("\n[3/4] 音声を生成しています...")
    updated_count = 0
    start_time = time.time()
    
    for w in target_works:
        no = w["no"]
        title = w["title_ja"]
        sec_prefix = f"{no:03d}"
        lines = w.get("lines", [])
        
        print(f"\n--- 第{no}段: 『{title}』({len(lines)}行) ---")
        
        # 出力ファイル名の決定
        ext = "mp3" if has_ffmpeg else "wav"
        gen_filename = f"{sec_prefix}_gen.{ext}"
        yaku_filename = f"{sec_prefix}_yaku.{ext}"
        
        gen_filepath = os.path.join(AUDIO_DIR, gen_filename)
        yaku_filepath = os.path.join(AUDIO_DIR, yaku_filename)
        
        rel_gen_url = f"audio/tsurezure/{gen_filename}"
        rel_yaku_url = f"audio/tsurezure/{yaku_filename}"
        
        # --- A. 原文朗読の生成 ---
        if os.path.exists(gen_filepath) and not force_all:
            print(f"  [スキップ] 原文音声は作成済みです: {gen_filename}")
        else:
            print(f"  [生成中] 原文朗読（発音表記・速度{SPEED_ORIGINAL}x）...")
            wav_chunks = []
            for l_idx, line in enumerate(lines):
                text_to_read = line.get("yomi") or line.get("text")
                query = create_audio_query(text_to_read, SPEAKER_ID, SPEED_ORIGINAL)
                w_bytes = synthesize_audio(query, SPEAKER_ID)
                wav_chunks.append(w_bytes)
            
            combined_wav = concatenate_wav_data(wav_chunks, pause_sec=PAUSE_BETWEEN_LINES)
            duration_sec = get_wav_duration_seconds(combined_wav)
            dur_str = format_duration(duration_sec)
            
            # 保存
            if has_ffmpeg:
                temp_wav = os.path.join(AUDIO_DIR, f"{sec_prefix}_gen_temp.wav")
                with open(temp_wav, "wb") as f:
                    f.write(combined_wav)
                if convert_wav_to_mp3(temp_wav, gen_filepath):
                    os.remove(temp_wav)
                else:
                    # 変換失敗時はWAVを維持
                    os.rename(temp_wav, gen_filepath.replace(".mp3", ".wav"))
                    rel_gen_url = rel_gen_url.replace(".mp3", ".wav")
            else:
                with open(gen_filepath, "wb") as f:
                    f.write(combined_wav)
            
            w["audio"]["original"]["url"] = rel_gen_url
            w["audio"]["original"]["duration"] = dur_str
            print(f"    -> 完了: {gen_filename} (再生時間: {dur_str})")
            updated_count += 1
        
        # --- B. ざっくり訳の生成 ---
        if os.path.exists(yaku_filepath) and not force_all:
            print(f"  [スキップ] 訳文音声は作成済みです: {yaku_filename}")
        else:
            print(f"  [生成中] ざっくり訳朗読（現代語・速度{SPEED_TRANSLATION}x）...")
            wav_chunks = []
            for l_idx, line in enumerate(lines):
                text_to_read = line.get("ja")
                if not text_to_read:
                    continue
                query = create_audio_query(text_to_read, SPEAKER_ID, SPEED_TRANSLATION)
                w_bytes = synthesize_audio(query, SPEAKER_ID)
                wav_chunks.append(w_bytes)
            
            combined_wav = concatenate_wav_data(wav_chunks, pause_sec=PAUSE_BETWEEN_LINES)
            duration_sec = get_wav_duration_seconds(combined_wav)
            dur_str = format_duration(duration_sec)
            
            # 保存
            if has_ffmpeg:
                temp_wav = os.path.join(AUDIO_DIR, f"{sec_prefix}_yaku_temp.wav")
                with open(temp_wav, "wb") as f:
                    f.write(combined_wav)
                if convert_wav_to_mp3(temp_wav, yaku_filepath):
                    os.remove(temp_wav)
                else:
                    os.rename(temp_wav, yaku_filepath.replace(".mp3", ".wav"))
                    rel_yaku_url = rel_yaku_url.replace(".mp3", ".wav")
            else:
                with open(yaku_filepath, "wb") as f:
                    f.write(combined_wav)
            
            w["audio"]["translation"]["url"] = rel_yaku_url
            w["audio"]["translation"]["duration"] = dur_str
            print(f"    -> 完了: {yaku_filename} (再生時間: {dur_str})")
            updated_count += 1

    # 5. データファイル書き戻し
    print("\n[4/4] 音声の再生時間をデータファイルへ反映しています...")
    save_dataset(dataset)
    print("  -> data/tsurezuregusa.js を更新しました。")
    
    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"  【全処理完了】 新規・更新生成: {updated_count}ファイル / 所要時間: {elapsed:.1f}秒")
    print(f"  音声保存先: {AUDIO_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
