#!/usr/bin/env python3
"""
viz_render.py — Folk Studio Visualizer
Calls fal.ai and Visoid APIs for architectural visualization.

MODES:
  concept  — Nano Banana 2 (fast concept, 30 sec, cheap)
  precise  — FLUX.1 Dev + ControlNet img2img (geometry-preserving, main tool)
  edit     — FLUX Kontext Pro (targeted material/style editing, 5 sec)
  final    — FLUX Pro Ultra (4K presentation renders)
  gpt      — GPT Image 2 (instruction-following, layout preservation) [MAIN]
  visoid   — Visoid API (architecture-tuned, 4K, good geometry, DAE/GLB upload)

Usage:
  # Quick concept from text only:
  python scripts/viz_render.py --prompt "..." --mode concept

  # Concept from photo/sketch:
  python scripts/viz_render.py --image sketch.jpg --prompt "..." --mode concept

  # Precise render from SketchUp export (preserves geometry):
  python scripts/viz_render.py --image model_monochrome.jpg --prompt "..." --mode precise

  # Precise render with ControlNet lineart (best geometry control):
  python scripts/viz_render.py --image model_depth.jpg --control lineart.jpg --prompt "..." --mode precise

  # Edit material in existing render:
  python scripts/viz_render.py --image render.jpg --prompt "change the wall to natural oak wood panels" --mode edit

  # Final 4K for client presentation:
  python scripts/viz_render.py --image render.jpg --prompt "..." --mode final --count 1

  # GPT Image 2 — best for instruction-following layout preservation:
  python scripts/viz_render.py --image model_color.jpg --control lineart.jpg --prompt "..." --mode gpt

  # Visoid — architecture-tuned, 4K, good with complex geometry:
  python scripts/viz_render.py --image model.jpg --prompt "..." --mode visoid
  python scripts/viz_render.py --image model.dae --prompt "..." --mode visoid   # 3D model upload
"""

import os
import sys
import json
import base64
import argparse
import requests
from pathlib import Path
from datetime import datetime


# fal.ai endpoints
ENDPOINTS = {
    "concept":      "fal-ai/nano-banana-2",
    "concept_pro":  "fal-ai/nano-banana-pro",
    "precise":      "fal-ai/flux-general/image-to-image",
    "precise_txt":  "fal-ai/flux-general",
    "edit":         "fal-ai/flux-kontext-pro",
    "final":        "fal-ai/flux-pro/v1.1-ultra",
    "gpt":          "openai/gpt-image-2/edit",
}

# Visoid REST API — architecture-tuned, 4K output, supports 3D model upload
# Docs: https://app.visoid.com/docs  (requires account)
VISOID_API_URL = "https://api.visoid.com/v1/render"  # TODO: verify exact URL from docs

CONTROLNET_CANNY = "InstantX/FLUX.1-dev-Controlnet-Canny"

# Optimized parameters per mode
# CRITICAL: FLUX uses guidance_scale 3.5, NOT 7.5 like Stable Diffusion
MODE_DEFAULTS = {
    "concept": {
        "num_inference_steps": 4,
        "guidance_scale": 5.0,
        "strength": 0.85,
    },
    "precise": {
        "num_inference_steps": 30,
        "guidance_scale": 3.5,
        "strength": 0.65,
        "controlnet_conditioning_scale": 0.55,
    },
    "edit": {
        "num_inference_steps": 28,
        "guidance_scale": 3.5,
        "strength": 0.75,
    },
    "final": {
        "num_inference_steps": 35,
        "guidance_scale": 3.5,
        "strength": 0.70,
    },
}


def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def render_visoid(
    prompt: str,
    image_path: str = None,
    count: int = 3,
) -> list:
    """
    Render via Visoid REST API.
    Requires VISOID_KEY in .env (get from app.visoid.com → Settings → API).

    Supported input formats: JPG, PNG, DAE, GLB (3D model files).
    Output: JPG up to 4K.

    Before using: confirm exact endpoint and payload fields at app.visoid.com/docs
    """
    load_env()
    visoid_key = os.getenv("VISOID_KEY")

    if not visoid_key:
        print("ERROR: VISOID_KEY not found. Add to .env:", file=sys.stderr)
        print("  VISOID_KEY=your_key_from_app.visoid.com", file=sys.stderr)
        return []

    out_dir = Path("output/renders")
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results = []
    is_3d_model = image_path and Path(image_path).suffix.lower() in (".dae", ".glb", ".obj")

    for i in range(count):
        print(f"  Generating variant {i + 1}/{count} [visoid]...", file=sys.stderr)

        headers = {
            "Authorization": f"Bearer {visoid_key}",
            # TODO: check docs — some APIs use "X-API-Key" instead of Bearer
        }

        try:
            if is_3d_model:
                # Upload 3D model as multipart — preserves exact geometry
                with open(image_path, "rb") as f:
                    files = {"model": (Path(image_path).name, f, "application/octet-stream")}
                    data = {
                        "prompt": prompt,
                        "quality": "high",
                        # TODO: check docs for supported style/material params
                    }
                    resp = requests.post(VISOID_API_URL, headers=headers, files=files, data=data, timeout=360)
            elif image_path:
                # Image-based render (JPG/PNG screenshot of model)
                payload = {
                    "prompt": prompt,
                    "image": image_to_base64(image_path),
                    "quality": "high",
                    # TODO: check docs for available style/material/season params
                }
                resp = requests.post(VISOID_API_URL, headers=headers, json=payload, timeout=360)
            else:
                # Text-to-render
                payload = {
                    "prompt": prompt,
                    "quality": "high",
                }
                resp = requests.post(VISOID_API_URL, headers=headers, json=payload, timeout=360)

            resp.raise_for_status()
            data = resp.json()

        except requests.exceptions.HTTPError:
            print(f"  HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
            if resp.status_code == 401:
                print("  → Check VISOID_KEY in .env", file=sys.stderr)
            elif resp.status_code == 402:
                print("  → Top up balance at app.visoid.com/billing", file=sys.stderr)
            elif resp.status_code == 422:
                print("  → Invalid payload. Check endpoint/params at app.visoid.com/docs", file=sys.stderr)
                print(f"  → Sent to: {VISOID_API_URL}", file=sys.stderr)
                print("  → If 422 persists: verify VISOID_API_URL constant at top of this file", file=sys.stderr)
            continue
        except requests.exceptions.Timeout:
            print("  → Timeout (>360s). Visoid may be processing — check app.visoid.com", file=sys.stderr)
            continue

        img_url = extract_image_url(data)
        if not img_url:
            print(f"  No image URL in response: {json.dumps(data)[:300]}", file=sys.stderr)
            print("  → Response format may differ from expected. Check docs.", file=sys.stderr)
            continue

        out_path = out_dir / f"render_visoid_{timestamp}_{i + 1}.jpg"
        try:
            download_image(img_url, out_path)
        except Exception as e:
            print(f"  Failed to download: {e}", file=sys.stderr)
            continue

        results.append(str(out_path))
        print(f"  ✓ {out_path}", file=sys.stderr)

    return results


def image_to_base64(path: str) -> str:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    ext = path.suffix.lstrip(".").lower()
    if ext == "jpg":
        ext = "jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/{ext};base64,{data}"


def download_image(url: str, out_path: Path) -> None:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(resp.content)


def build_payload(mode: str, prompt: str, image_path: str = None,
                  control_path: str = None, strength: float = None,
                  steps: int = None, guidance: float = None) -> dict:
    defaults = MODE_DEFAULTS.get(mode, MODE_DEFAULTS["concept"])

    # GPT Image 2 uses a completely different payload format
    if mode == "gpt":
        image_urls = []
        if image_path:
            image_urls.append(image_to_base64(image_path))
        if control_path:
            image_urls.append(image_to_base64(control_path))
            print("  GPT mode: lineart added as second reference image", file=sys.stderr)
        payload = {
            "prompt": prompt,
            "image_urls": image_urls,
            "quality": "high",
        }
        return payload

    payload = {
        "prompt": prompt,
        "num_inference_steps": steps or defaults["num_inference_steps"],
        "guidance_scale": guidance or defaults["guidance_scale"],
    }

    if image_path:
        payload["image_url"] = image_to_base64(image_path)
        payload["strength"] = strength or defaults["strength"]

    # ControlNet: lineart lock for precise geometry preservation (ArchiCAD/SketchUp → FLUX)
    if mode == "precise" and control_path:
        payload["controlnets"] = [{
            "path": CONTROLNET_CANNY,
            "control_image_url": image_to_base64(control_path),
            "conditioning_scale": defaults.get("controlnet_conditioning_scale", 0.55),
        }]
        print(
            f"  ControlNet: geometry lock active (scale={defaults.get('controlnet_conditioning_scale', 0.55)})",
            file=sys.stderr
        )

    return payload


def get_endpoint(mode: str, has_image: bool) -> str:
    if mode == "precise" and not has_image:
        return ENDPOINTS["precise_txt"]
    return ENDPOINTS.get(mode, ENDPOINTS["concept"])


def extract_image_url(data: dict) -> str | None:
    if "images" in data and data["images"]:
        return data["images"][0].get("url")
    if "image" in data:
        img = data["image"]
        return img.get("url") if isinstance(img, dict) else img
    if "output" in data:
        return data["output"]
    return None


def render(
    prompt: str,
    mode: str = "concept",
    image_path: str = None,
    control_path: str = None,
    count: int = 3,
    strength: float = None,
    steps: int = None,
    guidance: float = None,
) -> list:
    # Visoid has its own function — route directly
    if mode == "visoid":
        return render_visoid(prompt=prompt, image_path=image_path, count=count)

    load_env()
    fal_key = os.getenv("FAL_KEY")

    if not fal_key:
        print("ERROR: FAL_KEY not found. Check your .env file.", file=sys.stderr)
        sys.exit(1)

    endpoint = get_endpoint(mode, bool(image_path))
    url = f"https://fal.run/{endpoint}"

    headers = {
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json",
    }

    out_dir = Path("output/renders")
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results = []

    for i in range(count):
        payload = build_payload(
            mode=mode,
            prompt=prompt,
            image_path=image_path,
            control_path=control_path,
            strength=strength,
            steps=steps,
            guidance=guidance,
        )

        print(f"  Generating variant {i + 1}/{count} [{mode}]...", file=sys.stderr)

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=360)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.HTTPError:
            print(f"  HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
            if resp.status_code == 401:
                print("  → Check FAL_KEY in .env", file=sys.stderr)
            elif resp.status_code == 402:
                print("  → Top up balance at fal.ai/dashboard", file=sys.stderr)
            elif resp.status_code == 422:
                print("  → Invalid payload. Check image format or model parameters.", file=sys.stderr)
            continue
        except requests.exceptions.Timeout:
            print("  → Timeout (>360s). Try fewer steps or smaller image.", file=sys.stderr)
            continue

        img_url = extract_image_url(data)
        if not img_url:
            print(f"  No image in response: {json.dumps(data)[:300]}", file=sys.stderr)
            continue

        out_path = out_dir / f"render_{mode}_{timestamp}_{i + 1}.jpg"
        try:
            download_image(img_url, out_path)
        except Exception as e:
            print(f"  Failed to download: {e}", file=sys.stderr)
            continue

        results.append(str(out_path))
        print(f"  ✓ {out_path}", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Folk Studio — AI Architectural Visualizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  concept  Fast iterations (Nano Banana 2, ~30 sec). Good for exploring directions.
  precise  Geometry-preserving render (FLUX + ControlNet). Main tool for SketchUp exports.
  edit     Targeted edits on existing render (FLUX Kontext). Change one material in 5 sec.
  final    4K presentation quality (FLUX Pro Ultra). Use before sending to client.
  gpt      GPT Image 2 (via fal.ai). Best geometry preservation. Requires FAL_KEY.
  visoid   Visoid API. Architecture-tuned, 4K. Accepts JPG/PNG or DAE/GLB 3D models.
           Requires VISOID_KEY in .env (get at app.visoid.com → Settings → API).

Strength guide (FLUX modes only, not applicable to gpt/visoid):
  0.50-0.65  Stay close to source geometry
  0.65-0.75  Balanced transformation (default)
  0.80-0.90  Strong style change, geometry loosens
  0.90+      Mostly new image
        """
    )
    parser.add_argument("--prompt", required=True, help="Architectural prompt")
    parser.add_argument("--image", help="Source image (SketchUp export, photo, sketch)")
    parser.add_argument("--control", help="Lineart/edge image for ControlNet geometry lock (precise mode)")
    parser.add_argument("--mode", default="concept",
                        choices=["concept", "precise", "edit", "final", "gpt", "visoid"],
                        help="Rendering mode (default: concept)")
    parser.add_argument("--count", type=int, default=3, help="Number of variants (default: 3)")
    parser.add_argument("--strength", type=float, help="Transformation strength 0.5-1.0")
    parser.add_argument("--steps", type=int, help="Inference steps")
    parser.add_argument("--guidance", type=float, help="Guidance scale (FLUX default: 3.5)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    mode_desc = {
        "concept": "Nano Banana 2 — fast concept",
        "precise": "FLUX Dev + ControlNet — geometry-preserving",
        "edit":    "FLUX Kontext Pro — targeted editing",
        "final":   "FLUX Pro Ultra — 4K presentation",
        "gpt":     "GPT Image 2 — instruction-following, layout preservation",
        "visoid":  "Visoid API — architecture-tuned, 4K, DAE/GLB model upload",
    }

    print(f"\n🎨 Folk Studio Visualizer", file=sys.stderr)
    print(f"   Mode: {args.mode} ({mode_desc[args.mode]})", file=sys.stderr)
    print(f"   Variants: {args.count}", file=sys.stderr)
    if args.image:
        print(f"   Source: {args.image}", file=sys.stderr)
    if args.control:
        print(f"   ControlNet: {args.control}", file=sys.stderr)
    print(f"   Prompt: {args.prompt[:80]}...\n", file=sys.stderr)

    renders = render(
        prompt=args.prompt,
        mode=args.mode,
        image_path=args.image,
        control_path=args.control,
        count=args.count,
        strength=args.strength,
        steps=args.steps,
        guidance=args.guidance,
    )

    if not renders:
        print("\n❌ No renders generated. Check errors above.", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ Done — {len(renders)} variants:", file=sys.stderr)
    for path in renders:
        print(f"   → {path}", file=sys.stderr)

    if args.json:
        print(json.dumps({"renders": renders, "count": len(renders)}))
    else:
        for path in renders:
            print(path)


if __name__ == "__main__":
    main()
