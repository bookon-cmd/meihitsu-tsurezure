# 名筆（MEIHITSU）『徒然草』珠玉の名段選（フェーズ1 試作10段）

鎌倉時代末期（約700年前）に吉田兼好（兼好法師）によって著された日本三大随筆の最高峰『徒然草』から、特に親しまれている代表的な10段を厳選したプロトタイプWebアプリケーションです。

---

## 🌟 フェーズ1 収録段（全10段）

1. **序段（0）**: 『つれづれなるままに』— 心に浮かぶよしなしごと
2. **第7段（7）**: 『あだし野の露消ゆる時なく』— 限りある命だからこそ美しい
3. **第19段（19）**: 『折節の移り変るこそ』— 四季の移ろいと季節の情緒
4. **第52段（52）**: 『仁和寺にある法師』— 仁和寺の法師、石清水に参れず
5. **第89段（89）**: 『奥山に猫またといふものありて』— 夜道で化け猫に襲われた法師の正体
6. **第92段（92）**: 『ある人、弓射ることを習ふに』— 二本の矢を持つな、初心の戒め
7. **第109段（109）**: 『高名の木登りといひし男』— 木登りの名人が教える油断の戒め
8. **第137段（137）**: 『花はさかりに、月はくまなきをのみ見るものかは』— 散る桜・雲に隠れる月こそ美しい
9. **第150段（150）**: 『一の事を励み習はんとする人』— 恥を捨てて挑む者こそ上達する
10. **第155段（155）**: 『世に従はん人は』— 待ってはくれない時間の流れ

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
