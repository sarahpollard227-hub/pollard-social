# Pollard 9:16 template (Instagram/Facebook Stories and Reels)

Agreed 23 Nov 2026 after feedback that the banners clashed with Instagram's own overlays.
Revised 26 Nov 2026 from Sarah's Facebook Reel screenshots: full-screen viewers on tall phones crop
about 96px off each side, and the like/comment/share/save buttons sat on top of the footer text.
Feed carousels and cards (1080x1350) keep the original layout; this template is only for 1080x1920.

Layout (1080x1920):
- 0-250: clear (top bar, Story progress bar and profile row). Slide background only.
- 250-400: black header band with logo, blue rule underneath.
- 400-1320: content area, x 130-880. Below y 1050 keep anything important left of x 860 (Reel buttons).
  Story stickers go in the lower part (about y 900-1300).
- 1320-1470: blue footer band; text left-aligned from x 130, ending before x 860.
- 1470-1920: clear (Reel name, caption, audio and comment box; Story reply bar). Background and watermark only.
- Never put text outside x 120-960 (cropped on tall phones).

Use:
1. In this folder: `npm pack @fontsource/poppins @fontsource/marcellus`, untar each and rename `package` to `poppins` and `marcellus`.
2. Stories: `python3 stories.py spec.json outdir` (see examples/stories-*.json; classes: counter, kicker, h1, h2, body, small, cta, blue).
3. Reels: `python3 reel.py spec.json out.mp4` (see examples/wed-reel-*.json; silent 30fps H.264; items fade in at `at` seconds, optional `out`).
   The content area is narrower than before, so headings wrap more: break lines by hand and leave room between items.
4. Check: `python3 check_overlays.py frame.png out.png "label"` draws the Reels viewer's overlays (red) on a frame
   and crops the sides as a tall phone does. Run it on a frame from every scene and look at it before sending.
