# 日本のGDPと経済成長率 1960–2025｜可視化と分析

日本の名目GDP（ドル建て／円建て）、実質経済成長率、一人当たりGDP、人口を
1960年から2025年まで可視化し、時代区分ごとに分析する GitHub Pages サイト。

> **制作について**: このサイトは Muse Wonder を使って作成されました（データ取得・可視化・分析・公開）。

## 公開ページ

GitHub Pages で公開（`main` ブランチのルートを配信）。

## 内容

- KPI: 2025年の名目GDP 4.44兆ドル／663.8兆円、実質成長率 +1.19%、一人当たりGDP 35,951ドル
- チャート1: 名目GDP（ドル／円、期間切替つき）
- チャート2: 実質成長率と10年移動平均
- チャート3: 実質GDP指数（1960年=100）と一人当たりGDP
- チャート4: 時代区分別の平均成長率（高度成長 +8.9% → コロナ以降 +0.38%）
- 分析: 円建て最高値とドル建て縮小の乖離、潜在成長率約0.5%（IMF）、人口減少の影響
- 直近10年のデータ表、全期間の CSV / JSON ダウンロード

## データ出典

- 世界銀行 World Development Indicators（WDI）: `NY.GDP.MKTP.CD`、`NY.GDP.MKTP.CN`、
  `NY.GDP.MKTP.KD`、`NY.GDP.MKTP.KD.ZG`、`NY.GDP.PCAP.CD`、`SP.POP.TOTL`
- 内閣府 経済社会総合研究所「国民経済計算（GDP統計）」2025年10–12月期GDP速報（2次速報値）ほか
- IMF, *Japan: 2025 Article IV Consultation*（2025年4月）

注: 長期系列は WDI で統一しているため、内閣府の最新推計とは改定時期・基準の違いにより
同一暦年でも数値が異なる場合がある。

## データの再生成

```bash
python3 scripts/fetch_data.py
```

World Bank API から再取得し、`data/japan_gdp.json`、`data/japan_gdp.csv`、
`assets/data.js` を再生成する。

## ローカル確認

```bash
python3 -m http.server 8000
# http://localhost:8000 を開く
```

## 構成

```
index.html            ダッシュボード本体（Chart.js CDN）
assets/data.js        描画用データ（自動生成）
data/japan_gdp.csv    全期間データ
data/japan_gdp.json   全期間データ
scripts/fetch_data.py World Bank API からの再取得スクリプト
```
