# AliDikte — Kararlar

| Tarih | Konu | Karar | Gerekçe |
|---|---|---|---|
| 2026-10-20 | Temel | yusufipk/dikte fork'lanır, sıfırdan yazılmaz | Zaten Windows'ta çalışıyor, testli |
| 2026-10-20 | Ses | Yerel whisper, GPU (CUDA 12.4); 11.8 değil | 11.8 paketinde cublas64_11.dll yok, sessizce CPU'ya düşüyor |
| 2026-10-20 | Model | `ggml-large-v3-turbo-q5_0` | Türkçe için hız/kalite dengesi, 547 MB |
| 2026-10-20 | Temizleme | Claude API, Haiku 5.5, düşünme kapalı, temperature yok | Ucuz (~0,0003 $/dikte), hızlı; model temperature'ı reddediyor |
| 2026-10-20 | Modlar | İmla / Prompt / Ham; gösterge, tepsi, Ayarlar ve kısayolla seçilir | Ali'nin isteği |
| 2026-10-20 | Minibar | Kayıt göstergesine İ/P/H düğmeleri; odak alınmaz | Ali'nin tanımı |
| 2026-10-20 | Kısayollar | Ctrl+Space seçili mod, Ctrl+Shift+Space Prompt, Ctrl+Alt+R Ham | Ali'nin onayı (Ham tuşu çakışıyor, değişecek) |
| 2026-10-20 | Tabirler | Liste boş başlar, kullanımla dolar; Prompt modunda anlamına çevrilir | Ali'nin tercihi |
| 2026-10-20 | Varsayılan | Kodda temizleme varsayılanı OpenRouter kalır; Ali'nin ayarı `anthropic` | Upstream testleri ve birleştirmeler bozulmasın |
| 2026-10-20 | Doğrulama | `prompt` CLI fiili zaten var; mod fiilleri `dictate-prompt` / `dictate-raw` | Çakışma |
| 2026-10-20 | Fikir | Fikir modu yapıştırmaz; ham metni yakalama kimliğiyle `idea_dir`/YYYY-AA-GG.md'ye ekler | AliOS gelen-kutusu ve Fikir Kasası sözleşmesi |
| 2026-10-20 | AliOS | Sesli komut `Ctrl+Alt+A`, Claude Code `assistant_dir` = AliOS | Ali'nin onayı |
| 2026-10-20 | Dağıtım | Herkese açık fork Ali91Geyik/AliDikte (master); kurulum adı AliDikte, kimlik `io.github.ali91geyik.alidikte`, sürüm 1.0.0; CI yalnızca Windows derler | Ali'nin onayı |
