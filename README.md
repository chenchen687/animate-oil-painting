# Animate Oil Paintings

Transform oil paintings, especially Impressionist works, into immersive 5–10 second looping desktop wallpapers while preserving the original composition, brushwork, color relationships, and visual identity.

## What it does

The Skill designs motion separately for each subject. Flags respond to wind, water follows its own wave pattern, clouds drift directionally, smoke is transported and dispersed, plants bend from their roots, and human figures move through readable posture changes with stable contact points. This keeps people from developing the wave-like spatial distortion that can make them feel artificial.

## Repository structure

```text
animate-oil-painting/
├── agents/
│   └── openai.yaml
├── references/
│   ├── motion-and-qa.md
│   └── terrace-case.md
├── scripts/
│   ├── render_terrace.py
│   └── terrace_environment.py
├── README.md
└── SKILL.md
```

## Core principles

- Use a fixed camera and a 5–10 second seamless loop.
- Preserve the original painting as the visual source of truth.
- Use layered masks, background reconstruction, and stable occlusion boundaries.
- Give each subject its own timing, amplitude, pivot, and response delay.
- Keep figures anchored to their feet, chairs, props, and shadows.
- Keep plants anchored at their roots and let motion increase toward the tips.
- Use directional translation for clouds and smoke instead of water-like warping.
- Validate both the encoded video and the visual quality of the loop.

## Files

- [SKILL.md](https://github.com/chenchen687/animate-oil-painting/blob/main/SKILL.md) contains the main reusable Skill instructions.
- [openai.yaml](https://github.com/chenchen687/animate-oil-painting/blob/main/agents/openai.yaml) defines the Skill display name and default invocation prompt.
- [motion-and-qa.md](https://github.com/chenchen687/animate-oil-painting/blob/main/references/motion-and-qa.md) describes motion parameters, prompt structure, and visual checks.
- [terrace-case.md](https://github.com/chenchen687/animate-oil-painting/blob/main/references/terrace-case.md) documents the Claude Monet reference case and its implementation limits.
- [render_terrace.py](https://github.com/chenchen687/animate-oil-painting/blob/main/scripts/render_terrace.py) renders the calibrated Sainte-Adresse example.
- [terrace_environment.py](https://github.com/chenchen687/animate-oil-painting/blob/main/scripts/terrace_environment.py) contains the environment animation used by that example.

## Use the Skill

Install or copy this repository into your Codex skills directory, then invoke it with:

```text
$animate-oil-painting
```

Example request:

```text
Use $animate-oil-painting to turn this Impressionist oil painting into a natural 8-second looping desktop wallpaper.
```

The Skill first analyzes the painting and proposes a motion plan. When a sample is requested, it creates a fixed-camera loop and reports the output format, motion choices, and known limitations.

## Sainte-Adresse example

The included renderer is calibrated to Claude Monet’s *Terrace at Sainte-Adresse* from 1867. It preserves the full painting and animates the approved scene elements with a fixed camera.

The current example includes wind-driven flags and vegetation, directional cloud drift, sailing boats responding to the water, smoke moving with the wind, and staged figure motion. The figure treatment uses two-dimensional layered silhouettes with pivots and pauses. It is designed for readable posture and contact rather than full 3D character animation.

### Requirements

- Python 3.10 or later
- Pillow
- NumPy
- OpenCV Python bindings
- FFmpeg, or `imageio-ffmpeg`

### Render a sample

From the `scripts` directory, run:

```bash
python scripts/render_terrace.py \
  --input /path/to/reference.jpg \
  --output /path/to/wallpaper.mp4 \
  --ffmpeg /path/to/ffmpeg
```

The renderer produces a 10-second, 30 fps, silent H.264 MP4 at 1430 × 1080. It checks that the video can be decoded and verifies the loop endpoints before completing the output file.

The input must match the reference composition and boundaries used by the case-specific masks. A cropped image, framed photograph, or different painting requires new masks, support points, and background reconstruction.

## Quality checks

Before delivery, inspect the start frame, the largest motion, the main pauses, and the loop seam. Play the video for several consecutive cycles and check the following:

- figures keep their shape and remain connected to their supports
- flowers move from stable roots with varied timing
- clouds and smoke travel in a consistent direction
- flags remain attached to their poles
- water motion stays inside the water region
- boats and masts remain legible
- masks do not pull nearby rails, chairs, paths, or horizon lines
- no double image, sudden reversal, or exposed background appears at the loop seam

Successful decoding confirms that the file is playable. It does not by itself confirm that the motion feels natural.

## License and artwork sources

The Skill instructions and scripts in this repository are provided for reuse. The Sainte-Adresse example uses a public-domain artwork reference. Review the rights for any source image before distributing a generated wallpaper.
