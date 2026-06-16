"""
rtl.py — Arabic / RTL text helper for Pygame

Pygame renders text strictly left-to-right and does not reshape Arabic
letters into their contextual forms. This module fixes both issues:
  1. arabic_reshaper  → joins letters into their contextual (connected) glyphs
  2. bidi algorithm   → reverses the visual order for RTL display

Usage:
    from rtl import ar
    surf = font.render(ar("كِسرة"), True, color)
"""

try:
    import arabic_reshaper
    from bidi.algorithm import get_display as _bidi

    def ar(text: str) -> str:
        """Return text reshaped and BiDi-reordered for correct Pygame rendering."""
        return _bidi(arabic_reshaper.reshape(text))

except ImportError:
    def ar(text: str) -> str:
        """Fallback: reverse the string (approximate RTL without reshaping)."""
        return text[::-1]
