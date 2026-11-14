# 名筆（MEIHITSU）『徒然草』（全244段：序段＋第1〜243段 完本）

鎌倉時代末期（約700年前）に吉田兼好（兼好法師）によって著された日本三大随筆の最高峰『徒然草』全244段（序段＋第1段〜第243段）を完全収録した古典鑑賞Webアプリケーションです。

---

## 🌟 構成・特徴

* **全244段完全収録**: 序段から第243段まで漏れなく網羅。
* **原文・音声用発音表記（yomi）・平易なざっくり現代語訳**: 全段にオリジナル書き下ろし現代語訳と注釈・見出し・季節タグを完備。
* **VOICEVOX一括自動生成対応**: 段数アナウンス（「じょだん。」「だいいちだん。」等）＋朗読本文を滑らかに合成。
* **珠玉の代表名段も即座に検索可能**: 仁和寺の法師（52段）、猫また（89段）、弓を射る法（92段）、木登りの名人（109段）、花は盛りに（137段）、百日の鯉（231段）、丹波の出雲（236段）、兼好幼少期の問答（243段）など。

---

## 🔒 著作権・権利の安全性（100%パブリックドメイン）

* **原文**: 国立国会図書館デジタルコレクション所蔵のパブリックドメイン刊本（大正14年『校註日本文学大系』および明治36年『国文大観』）を直接照合し、現代の校注本等の著作権物は一切使用していません。
  * 字句の異同・検討語の一覧は [`TEXT_COMPARISON.md`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/TEXT_COMPARISON.md) に記録されています。
* **現代語訳（ざっくり訳）**: 原文から直接書き起こした名筆オリジナルの平易な現代語訳です。
* **音声**: VOICEVOXエンジンによるローカル生成（またはWeb Speech APIフォールバック）。

---

## 🎙 音声生成（VOICEVOX）の手順

ご自身のパソコンでVOICEVOXを起動し、以下のファイルをダブルクリックするだけで音声（原文・ざっくり訳の2種）が一括生成されます。

* **Mac**: [`generate_audio.command`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/generate_audio.command) をダブルクリック
* **Windows**: [`generate_audio.bat`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/generate_audio.bat) をダブルクリック

詳しい使い方は [`VOICEVOX_GUIDE.md`](file:///Users/aizawakenichi/anti-gravity/meihitsu-tsurezure/VOICEVOX_GUIDE.md) をご覧ください。

---

## 📱 WordPress 埋め込み用コード (`https://tools.book-on.pro/meihitsu/tsurezure/`)

```html
<style>
/* Cocoon ブログ枠・装飾の完全除去 */
#header-container, #header, .header-container,
.article-header, .entry-title, .date-tags,
#sidebar, .article-footer, #footer-container, #footer,
#breadcrumb, .mobile-footer-buttons-wrap, .sns-share, .sns-follow,
.author-info, .entry-categories, .entry-tags {
  display: none !important;
}
body, html {
  background: #0d0c0a !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
  height: 100% !important;
}
#content, #content-in, #main, .article {
  width: 100vw !important;
  max-width: 100vw !important;
  height: 100vh !important;
  padding: 0 !important;
  margin: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
.meihitsu-app-frame {
  width: 100vw;
  height: 100vh;
  border: none;
  display: block;
}
</style>

<iframe 
  class="meihitsu-app-frame" 
  src="https://<YOUR-CLOUDFLARE-URL>/" 
  allow="autoplay"
  title="名筆 - 徒然草 名段選">
</iframe>
```
