"""Fikir mode: a dictation kept as an idea rather than pasted.

The line follows the Fikir Kasası capture contract that AliOS's inbox is read
under: the text exactly as it was heard, a capture id made at the moment of
capture so that moving it into the vault later never makes a second record,
and the channel and source it came in through. One line per idea, appended to
the day's file, so that nothing written before is ever rewritten.
"""

import pathlib
import secrets
import time

CHANNEL = "Bilgisayar dikte"
SOURCE = "Dikte"


def default_dir():
    return pathlib.Path.home() / "Documents" / "AliDikte" / "Fikirler"


def folder(conf):
    chosen = (conf.get("idea_dir") or "").strip()
    return pathlib.Path(chosen).expanduser() if chosen else default_dir()


def capture_id(now=None):
    """yk-YYYYMMDD-HHMMss-xxxx, the vault's own shape for one."""
    now = time.localtime() if now is None else now
    return f"yk-{time.strftime('%Y%m%d-%H%M%S', now)}-{secrets.token_hex(2)}"


def line(text, now=None, ident=None):
    now = time.localtime() if now is None else now
    ident = ident or capture_id(now)
    # One idea, one line: the inbox is read line by line. Only the whitespace is
    # touched; the words stay as they were heard.
    flat = " ".join(text.split())
    return (f"- [{time.strftime('%H:%M', now)}] (fikir) {flat} "
            f"<!-- yk:{ident} kanal:{CHANNEL} kaynak:{SOURCE} -->")


def save(text, conf, now=None):
    """Append the idea to the day's file; the file it went into."""
    now = time.localtime() if now is None else now
    target = folder(conf) / f"{time.strftime('%Y-%m-%d', now)}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(line(text, now) + "\n")
    return target
