#!/usr/bin/env python3
"""
patch_web.py — Replace Pygbag's default ugly loading screen with an Egyptian-themed one.

Usage: python3 tools/patch_web.py build/web/index.html
"""
import sys, re

path = sys.argv[1] if len(sys.argv) > 1 else "build/web/index.html"
html = open(path, encoding="utf-8").read()

# ── 1. Replace body background (powderblue → deep Egyptian dark) ──────────────
html = html.replace("background-color:powderblue;", "background-color:#05050F;")
html = html.replace("background-color: powderblue;", "background-color:#05050F;")

# ── 2. Replace the infobox style (green bg / blue text → gold on dark) ────────
old_infobox = """        #infobox {
            position: fixed; /* center relative to viewport */
            background: green;
            color: blue;
            font-weight: bold;
            padding: 12px 24px;
 /*           display: none; */
            z-index: 999999;
        }"""

new_infobox = """        #infobox {
            position: fixed;
            background: rgba(5,5,18,0.95);
            color: #FFD700;
            font-weight: bold;
            font-family: Georgia, serif;
            font-size: 18px;
            letter-spacing: 2px;
            padding: 18px 36px;
            border: 2px solid #FFD700;
            border-radius: 4px;
            box-shadow: 0 0 30px rgba(255,215,0,0.25);
            z-index: 999999;
        }"""

html = html.replace(old_infobox, new_infobox)

# ── 3. Replace "Loading, please wait ..." text ────────────────────────────────
html = html.replace(
    "<div id=\"infobox\">Loading, please wait ...</div>",
    "<div id=\"infobox\">⚱ KESRA &mdash; Loading &hellip;</div>"
)

# ── 4. Add a full-page Egyptian loading overlay before </body> ────────────────
loading_overlay = """
<style>
#kesra-splash {
    position: fixed; inset: 0;
    background: radial-gradient(ellipse at 50% 60%, #1a0a2e 0%, #05050F 70%);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    z-index: 99998;
    transition: opacity 1s ease;
}
#kesra-splash h1 {
    color: #FFD700;
    font-family: Georgia, serif;
    font-size: clamp(48px, 10vw, 96px);
    letter-spacing: 8px;
    margin: 0 0 8px 0;
    text-shadow: 0 0 40px rgba(255,215,0,0.6);
}
#kesra-splash p {
    color: #b8943f;
    font-family: Georgia, serif;
    font-size: clamp(14px, 3vw, 20px);
    letter-spacing: 4px;
    margin: 0 0 48px 0;
}
#kesra-bar-wrap {
    width: min(320px, 70vw);
    height: 4px;
    background: #1a1a1a;
    border-radius: 2px;
    overflow: hidden;
}
#kesra-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #b8943f, #FFD700, #b8943f);
    border-radius: 2px;
    animation: kesra-pulse 2s ease-in-out infinite;
}
@keyframes kesra-pulse { 0%,100%{opacity:.6} 50%{opacity:1} }
#kesra-pyramids {
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 120px; overflow: hidden;
}
</style>
<div id="kesra-splash">
    <svg id="kesra-pyramids" viewBox="0 0 480 120" preserveAspectRatio="xMidYMax slice"
         xmlns="http://www.w3.org/2000/svg">
        <polygon points="60,120 130,20 200,120" fill="#12082a" stroke="#3a2a00" stroke-width="1"/>
        <polygon points="280,120 350,10 420,120" fill="#12082a" stroke="#3a2a00" stroke-width="1"/>
        <polygon points="160,120 215,50 270,120" fill="#0e061f" stroke="#3a2a00" stroke-width="1"/>
    </svg>
    <h1>KESRA</h1>
    <p>EGYPTIAN BRICK-BREAKER</p>
    <div id="kesra-bar-wrap"><div id="kesra-bar"></div></div>
</div>
<script>
(function(){
    var bar = document.getElementById('kesra-bar');
    var splash = document.getElementById('kesra-splash');
    var w = 0;
    var iv = setInterval(function(){
        w = Math.min(w + Math.random() * 3, 95);
        bar.style.width = w + '%';
    }, 120);
    // Hide splash once the game canvas becomes visible
    var obs = new MutationObserver(function(){
        var canvas = document.getElementById('canvas');
        if (canvas && canvas.style.visibility === 'visible') {
            clearInterval(iv);
            bar.style.width = '100%';
            setTimeout(function(){
                splash.style.opacity = '0';
                setTimeout(function(){ splash.remove(); }, 1000);
            }, 300);
            obs.disconnect();
        }
    });
    obs.observe(document.body, {attributes:true, subtree:true, attributeFilter:['style']});
})();
</script>
"""

html = html.replace("</body>", loading_overlay + "\n</body>")

# ── 5. Fix title ──────────────────────────────────────────────────────────────
html = html.replace("<title>kesra</title>",
                    "<title>Kesra — Egyptian Brick-Breaker</title>")

open(path, "w", encoding="utf-8").write(html)
print(f"Patched: {path}")
