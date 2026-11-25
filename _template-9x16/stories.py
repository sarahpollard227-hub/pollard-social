"""Render Instagram Story backgrounds (1080x1920) in the 9:16 safe-zone template.
Usage: python3 stories.py <spec.json> <outdir>
spec: [{"file":"sun-story-1.png","theme":"black","html":"..."}]"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).parent.resolve()
spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto((here / "vertical.html").as_uri())
    for s in spec:
        pg.evaluate("([t,h]) => renderStatic(t,h)", [s["theme"], s["html"]])
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(150)
        pg.screenshot(path=str(out / s["file"]))
        print("wrote", s["file"])
    b.close()
