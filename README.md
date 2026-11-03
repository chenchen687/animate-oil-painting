# Animate Oil Paintings

Transform oil paintings, especially Impressionist works, into immersive 5–10 second looping desktop wallpapers. The project preserves the original composition, brushwork, color relationships, and visual identity while adding carefully directed motion to flags, water, clouds, smoke, vegetation, sailing boats, shadows, and human figures.

## What it does

The Skill analyzes the visual structure of a painting before animation begins. It identifies wind direction, water movement, object boundaries, support points, occlusion order, lighting, and the parts of the image that can move safely.

Motion is designed per subject rather than applied as a single distortion field. Plants stay rooted and bend from the stem. Clouds travel through the sky with directional drift. Smoke is transported and dispersed by the wind. People move through readable posture changes with joints, pauses, contact points, and delayed responses. This keeps human figures from developing the wave-like spatial warping that can make them feel artificial.

## Core principles

- Use a fixed camera and a 5–10 second seamless loop.
- Preserve the original painting as the visual source of truth.
- Use layered masks, background reconstruction, and stable occlusion boundaries.
- Give each subject its own timing, amplitude, pivot, and response delay.
- Keep figures anchored to their feet, chairs, props, and shadows.
- Keep plants anchored at their roots and let motion increase toward the tips.
- Use directional translation for clouds and smoke instead of water-like warping.
- Validate both the encoded video and the visual quality of the loop.

## Included Skill

The reusable Skill is located at [`outputs/animate-oil-painting/SKILL.md`](outputs/animate-oil-painting/SKILL.md). It includes:

- motion analysis and prompt-writing guidance
- character, vegetation, cloud, smoke, flag, and water animation rules
- loop design and visual quality checks
- desktop wallpaper output guidance
- a dedicated Sainte-Adresse reference case

The Skill package is also available as [`outputs/animate-oil-painting.zip`](outputs/animate-oil-painting.zip).

## Example

The first reference case is Claude Monet’s *Terrace at Sainte-Adresse* from 1867. The working sequence develops the scene in stages, keeping the approved flag, water, and vegetation motion while refining the figures, clouds, and smoke.

The latest sample is [`Terrace-at-Sainte-Adresse-v7.mp4`](outputs/Terrace-at-Sainte-Adresse-v7.mp4).

The final sample uses a complete 1430 × 1080 frame without side borders. It includes wind-driven flags and plants, directional cloud drift, sailing boats responding to the water, smoke moving with the wind, and staged figure motion. The figure animation remains a two-dimensional layered treatment, so it should be evaluated for readable posture and contact rather than interpreted as full 3D character animation.

## Sainte-Adresse renderer

The included renderer is calibrated to the provided Sainte-Adresse reference image. It is a case-specific example, not an automatic animation system for arbitrary paintings.

### Requirements

- Python 3.10 or later
- Pillow
- NumPy
- OpenCV Python bindings
- FFmpeg, or `imageio-ffmpeg`

### Render a sample

From the Skill directory, run:

```bash
python scripts/render_terrace.py \
  --input /path/to/reference.jpg \
  --output /path/to/wallpaper.mp4 \
  --ffmpeg /path/to/ffmpeg
```

The renderer produces a 10-second, 30 fps, silent H.264 MP4 at 1430 × 1080. It writes a temporary file, checks that the video can be decoded, verifies the loop endpoints, and then moves the completed file into the requested output path.

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

Successful decoding only confirms that the file is playable. Natural motion still requires visual inspection at normal desktop viewing size.

## Project status

This repository contains the reusable Skill, its supporting references, and the Sainte-Adresse example renderer. The general workflow supports new oil paintings through fresh visual analysis and newly prepared masks. The bundled renderer remains specific to the Monet reference case.
