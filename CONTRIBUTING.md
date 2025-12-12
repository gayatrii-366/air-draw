# Contributing to Air-Draw

Thank you for your interest in improving this project!

## 💻 How to Contribute

### 1. Fork the repository
Click "Fork" on GitHub and clone your copy.

### 2. Create a feature branch
Follow our naming conventions:
- `feat/<feature-name>`
- `fix/<bug-name>`
- `refactor/<module-name>`

### 3. Commit using conventional messages
Examples:
- `feat: add depth-based smoothing`
- `fix: hand jitter on low light`
- `docs: update readme`

### 4. Run tests before pushing
```bash
pytest

feat: complete AirDraw v1.0 (UI, neon engine, smoothing, palette, gestures)

Description

This PR finalises the AirDraw v1.0 release.

It upgrades the entire app into a clean, polished, user-friendly hand-tracking drawing tool with neonstrokes, smoothing, gesture controls, and UI enhancements.
What problem was solved?
Previously, the app had:
Jittery, unstable lines
No clear UI or colour feedback
Pinch-only drawing
No documentation or contribution structure
This PR solves all of those issues by adding:
Index-finger-only drawing (more natural)
Neon glow stroke engine
Exponential smoothing for stable lines
Colour palette overlay with number labels
Keyboard colour switching (1/2/3/4 + C)
Fist gesture to clear canva
FPS display + title bar
Clean folder structure

###5. OPen a pull request
Release preparation for v1.0
The project is now ready for public use and contributions.
What features were added?
Neon glow effect using layered strokes
Smoothing filter for point tracking
Colour palette with active highlight
User colour input (1–4 keys)
Clear gesture (fist)
UI overlays: FPS, title, thickness
Modular engine (draw_engine.py)
Gesture utils (fingers.py, gestures.py)
Contribution guide
Changelog v1.0
How to test
Run:
python air_draw_app.py
Confirm these behaviours:
Raise index finger → smooth neon drawing
Lower finger → drawing stops
Press 1/2/3/4 → palette updates + colour changes
Press C → cycles colours
Make a fist → canvas clears
Observe FPS and UI indicators
Check that:
The colour highlight works correctly
Neon blur looks smooth
No jitter in strokes
No errors during runtime


6. Click **Publish Release**

This gives your project a proper versioned identity.

---

# ✅ **STEP 3 — Add Demo GIF (most important)**

People always check the demo first.

### Make a recording:
1. Open `air_draw_app.py`
2. Record your screen using OBS / Xbox Game Bar (Win + G)
3. Draw for 5–6 seconds:
   - Switch colours  
   - Clear canvas  
   - Show finger drawing  

Save the video.

### Convert to GIF online:
Upload to any converter:
- ezgif.com  
- cloudconvert  
- adobe express  

Resize to width **600px**.

### Add GIF to README:
Upload GIF to your GitHub repo under `assets/` folder.

Then add this to README.md top section:

```markdown
<p align="center">
  <img src="assets/demo.gif" width="600px" alt="Air Draw Demo">
</p>
