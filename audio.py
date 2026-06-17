"""
audio.py — zero-dependency procedural sound effects.

All SFX are synthesised at runtime from sine/square tones (no audio files, no numpy)
and cached as pygame.mixer.Sound objects. Everything is wrapped in broad try/except:
audio is strictly optional, and on platforms where the mixer is unavailable (e.g. the
Pygbag/WASM sandbox before a user gesture) the whole module silently no-ops instead of
crashing the game.

Public API:
    init()              — set up the mixer + build the SFX bank (call once at startup)
    set_muted(bool)     — toggle mute
    play(name)          — play a named one-shot
    play_brick(combo)   — brick-hit blip whose pitch rises with the combo
"""
import math
from array import array

_RATE = 22050
enabled = False
muted   = False

_sounds: dict = {}
_brick_sounds: list = []


def init() -> None:
    """Initialise the mixer (re-initialising if needed) and build the SFX bank."""
    global enabled
    try:
        import pygame
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        pygame.mixer.init(_RATE, -16, 1, 512)
        pygame.mixer.set_num_channels(16)
        _build()
        enabled = True
    except Exception:
        enabled = False


def set_muted(value: bool) -> None:
    global muted
    muted = bool(value)


# ── synthesis ─────────────────────────────────────────────────────────────────
def _seq(notes, vol=0.35, wave="sine"):
    """Build a Sound from a list of (freq_hz, duration_s) notes played in sequence."""
    import pygame
    buf = array("h")
    for freq, dur in notes:
        n = max(1, int(_RATE * dur))
        for i in range(n):
            t   = i / _RATE
            env = 1.0 - i / n                      # linear decay per note
            if freq <= 0:                           # rest
                buf.append(0)
                continue
            if wave == "square":
                s = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
            else:
                s = math.sin(2 * math.pi * freq * t)
            buf.append(int(max(-1.0, min(1.0, s * env * vol)) * 32767))
    return pygame.mixer.Sound(buffer=buf.tobytes())


def _build() -> None:
    _sounds.clear()
    _brick_sounds.clear()

    # paddle bounce — short low square "thock"
    _sounds["paddle"]   = _seq([(196, 0.06)], vol=0.4, wave="square")
    # drop / coin collect — bright two-note chime
    _sounds["coin"]     = _seq([(880, 0.05), (1320, 0.07)], vol=0.3)
    # power-up — rising arpeggio
    _sounds["power"]    = _seq([(523, 0.05), (659, 0.05), (784, 0.08)], vol=0.32)
    # combo milestone — bright chord-ish run
    _sounds["combo"]    = _seq([(784, 0.05), (988, 0.05), (1175, 0.1)], vol=0.34)
    # life lost — descending tone
    _sounds["lose"]     = _seq([(330, 0.12), (247, 0.12), (165, 0.18)], vol=0.4, wave="square")
    # round clear — triumphant ascending fanfare
    _sounds["clear"]    = _seq([(523, 0.09), (659, 0.09), (784, 0.09), (1047, 0.18)], vol=0.36)
    # game over — slow low descent
    _sounds["over"]     = _seq([(220, 0.22), (165, 0.22), (110, 0.4)], vol=0.42, wave="square")
    # explosion (bomb/rocket) — low square burst
    _sounds["boom"]     = _seq([(140, 0.05), (90, 0.12)], vol=0.45, wave="square")

    # brick-hit blips — pitch climbs with the combo count
    base = [294, 330, 370, 415, 466, 523, 587, 659, 740, 831, 932, 1047]
    for f in base:
        _brick_sounds.append(_seq([(f, 0.045)], vol=0.28))


# ── playback ──────────────────────────────────────────────────────────────────
def play(name: str) -> None:
    if not enabled or muted:
        return
    s = _sounds.get(name)
    if s is not None:
        try:
            s.play()
        except Exception:
            pass


def play_brick(combo: int) -> None:
    if not enabled or muted or not _brick_sounds:
        return
    idx = max(0, min(combo, len(_brick_sounds) - 1))
    try:
        _brick_sounds[idx].play()
    except Exception:
        pass
