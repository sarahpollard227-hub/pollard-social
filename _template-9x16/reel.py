"""Render a text-on-screen Reel (1080x1920, silent MP4) in the 9:16 safe-zone template.
Usage: python3 reel.py <spec.json> <out.mp4>
spec: {"duration":26,"scenes":[{"start":0,"end":3.5,"theme":"black",
        "items":[{"html":"...","at":0.2,"out":null,"style":"top:110px"}]}]}
Each item fades in (0.45s, rising 24px) at `at` seconds and, if `out` is set, fades out then.
Item `style` positions it absolutely inside the content area (x 130-880, y 400-1320)."""
import json, sys, pathlib, subprocess, tempfile, shutil
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).parent.resolve()
spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
out_mp4 = pathlib.Path(sys.argv[2]).resolve()
FPS = 30
JS = r"""
(spec) => {
  const root = document.getElementById('root');
  root.innerHTML = '';
  spec.scenes.forEach((sc, i) => {
    const d = document.createElement('div');
    d.innerHTML = `<div class="slide ${sc.theme}" id="sc${i}"><div class="wm"></div>` +
      HEADER + `<div class="content">` +
      sc.items.map((it, j) => `<div class="it" id="it${i}_${j}" style="position:absolute;left:0;right:0;${it.style||''}">${it.html}</div>`).join('') +
      `</div>` + FOOTER + `</div>`;
    root.appendChild(d.firstChild);
  });
  window.setT = (t) => {
    spec.scenes.forEach((sc, i) => {
      const el = document.getElementById('sc'+i);
      const XF = 0.25;
      let o = 0;
      if (t >= sc.start && t < sc.end) o = i === 0 ? 1 : Math.min(1, (t - sc.start) / XF);
      else if (t >= sc.end && i < spec.scenes.length - 1 && t < sc.end + XF) o = 1; // stays under the next scene while it fades in
      else if (t >= sc.end && i === spec.scenes.length - 1) o = 1;
      el.style.opacity = o; el.style.zIndex = i; el.style.display = o > 0 ? 'block' : 'none';
      sc.items.forEach((it, j) => {
        const e = document.getElementById(`it${i}_${j}`);
        const lt = t - sc.start;
        let a = Math.max(0, Math.min(1, (lt - it.at) / 0.45));
        a = 1 - Math.pow(1 - a, 3);
        let b = 1;
        if (it.out != null) b = 1 - Math.max(0, Math.min(1, (lt - it.out) / 0.3));
        e.style.opacity = a * b;
        e.style.transform = `translateY(${(1 - a) * 24}px)`;
      });
    });
  };
}
"""
tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto((here / "vertical.html").as_uri())
    pg.evaluate(JS, spec)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)
    n = int(round(spec["duration"] * FPS))
    for f in range(n):
        pg.evaluate(f"setT({f / FPS})")
        pg.screenshot(path=str(tmp / f"f{f:05d}.png"))
    b.close()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%05d.png"),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", "-an", str(out_mp4)], check=True)
shutil.rmtree(tmp)
print("wrote", out_mp4, n, "frames")
