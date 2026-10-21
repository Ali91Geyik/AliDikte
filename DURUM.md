# AliDikte — Durum

Son güncelleme: 2026-10-20

## Sürüm 1 tamam
- Fork: yusufipk/dikte 2.2.0 → `ali` dalı
- Doğrudan Claude API temizleme sağlayıcısı (`anthropic`, varsayılan model `claude-haiku-5-5`, düşünme kapalı)
- Dikte modları: İmla / Prompt / Ham; kayıt göstergesinde İ/P/H düğmeleri, tepsi alt menüsü, Ayarlar'da Mod kutusu
- Mod kısayolları: `dictate-prompt` (Ctrl+Shift+Space), `dictate-raw` (Ctrl+Alt+R)
- Kişisel tabirler (`personal_style`): İmla korur, Prompt anlamını yazar
- Fikir modu (F): ham metin + yakalama kimliği, `idea_dir` altında günün dosyası
- Kurulum adı AliDikte, sürüm 1.0.0, güncellemeler Ali91Geyik/AliDikte'den
- Windows + NVIDIA: whisper.cpp CUDA 12.4 derlemesi indirilir; Ayarlar "CUDA" gösterir
- Ölçüm: 8 sn ses GPU'da ~4,5 sn (açılış dahil); ilk gerçek dikte 4,2 sn ses → 1,3 sn (temizleme dahil)

## Sürüm 1.1
- Claude köprüsü (Ayarlar → Agent → "Claude köprüsü"): komut Prompt modunda düzenlenir, AliOS'ta Claude Code'a gider; cevap panelde (Kopyala, Terminalde devam et → `wt claude --resume`)
- Kurulum: masaüstü kısayolu (varsayılan açık), açılışta başlama; açılışta "Hazır" bildirimi

## Yayın
- v1.0.0: https://github.com/Ali91Geyik/AliDikte/releases/tag/v1.0.0 (AliDikte-1.0.0-x64-setup.exe, 48 MB, GitHub Actions)
- Yeni sürüm: `__version__`'ı artır, `vX.Y.Z` etiketi it; upstream etiketleri çekilmez (`remote.upstream.tagOpt --no-tags`)
- AliOS bağlantısı Ali'nin makinesinde ayarlı (`aliOS-bagla.ps1`)

## Açık işler
- [ ] Ham kısayolu: `Ctrl+Alt+R` başka programda; yeni tuş Ali'de

## Bilinen
- 4 Homebrew testi Windows'ta sembolik bağ izni olmadığı için hata verir (upstream'de de böyle)
- Claude masaüstünden çalışan komutların AppData yazmaları yönlendirilir; kurulum ve ayar Ali'nin kendi PowerShell'inden (`veri-tasi.ps1` örneği, repoda değil)
