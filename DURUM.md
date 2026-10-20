# AliDikte — Durum

Son güncelleme: 2026-10-20

## Sürüm 1 tamam
- Fork: yusufipk/dikte 2.2.0 → `ali` dalı
- Doğrudan Claude API temizleme sağlayıcısı (`anthropic`, varsayılan model `claude-haiku-5-5`, düşünme kapalı)
- Dikte modları: İmla / Prompt / Ham; kayıt göstergesinde İ/P/H düğmeleri, tepsi alt menüsü, Ayarlar'da Mod kutusu
- Mod kısayolları: `dictate-prompt` (Ctrl+Shift+Space), `dictate-raw` (Ctrl+Alt+R)
- Kişisel tabirler (`personal_style`): İmla korur, Prompt anlamını yazar
- Windows + NVIDIA: whisper.cpp CUDA 12.4 derlemesi indirilir; Ayarlar "CUDA" gösterir
- Ölçüm: 8 sn ses GPU'da ~4,5 sn (açılış dahil); ilk gerçek dikte 4,2 sn ses → 1,3 sn (temizleme dahil)

## Açık işler
- [ ] Ham kısayolu: `Ctrl+Alt+R` başka programda; yeni tuş Ali'de
- [ ] AliOS bağlantıları: sesli komut → AliOS klasöründe Claude Code; "Fikir" modu → gelen-kutusu
- [ ] GitHub reposu (Ali91Geyik) ve paylaşılabilir Windows kurulum dosyası
- [ ] Güncelleme denetimi upstream'e bakıyor (`dikte/update.py`); fork'un reposuna çevrilmeli

## Bilinen
- 4 Homebrew testi Windows'ta sembolik bağ izni olmadığı için hata verir (upstream'de de böyle)
- Claude masaüstünden çalışan komutların AppData yazmaları yönlendirilir; kurulum ve ayar Ali'nin kendi PowerShell'inden (`veri-tasi.ps1` örneği, repoda değil)
