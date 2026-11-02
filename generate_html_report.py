from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def humanize(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").strip().title()


def render_value(value: Any, key: str = "") -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if value is None:
        return "Not available"
    if isinstance(value, float):
        return f"{value:.4f}" if abs(value) < 1 else f"{value:,.3f}"
    if isinstance(value, (int, str)):
        return html.escape(str(value))
    if isinstance(value, list):
        if not value:
            return "None"
        return "<ul>" + "".join(f"<li>{render_value(item)}</li>" for item in value) + "</ul>"
    if isinstance(value, dict):
        return render_table(value)
    return html.escape(str(value))


def render_table(data: dict[str, Any]) -> str:
    rows = []
    for key, value in data.items():
        if isinstance(value, dict):
            rows.append(
                f'<tr><th colspan="2" class="group">{html.escape(humanize(str(key)))}</th></tr>'
                f'<tr><td colspan="2">{render_table(value)}</td></tr>'
            )
        else:
            rows.append(
                f"<tr><th>{html.escape(humanize(str(key)))}</th>"
                f"<td>{render_value(value, str(key))}</td></tr>"
            )
    return '<table><tbody>' + "".join(rows) + "</tbody></table>"


def find_images(report_path: Path) -> list[Path]:
    root = report_path.parent
    images = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            if path.name.lower() not in {"original.jpg", "original.png"}:
                images.append(path)
    return images


def build_report(json_path: Path, output_path: Path | None = None) -> Path:
    json_path = json_path.resolve()
    if not json_path.exists():
        raise FileNotFoundError(f"Could not find JSON report: {json_path}")

    with json_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        data = {"analysis_results": data}

    output_path = output_path or json_path.with_name("report.html")
    output_path = output_path.resolve()

    title = data.get("title") or data.get("project") or "TRACE-X Image Analysis"
    source = data.get("input") or data.get("image") or data.get("source") or "Not specified"
    created = data.get("created_at") or data.get("timestamp") or datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")

    images_html = []
    for image_path in find_images(json_path):
        try:
            relative = image_path.relative_to(output_path.parent)
        except ValueError:
            relative = image_path
        label = humanize(image_path.stem)
        images_html.append(
            f'<figure><img src="{html.escape(relative.as_posix())}" alt="{html.escape(label)}">'
            f'<figcaption>{html.escape(label)}</figcaption></figure>'
        )

    images_section = (
        '<section><h2>Visual evidence</h2><div class="gallery">'
        + "".join(images_html)
        + "</div></section>"
        if images_html
        else ""
    )

    body = render_table(data)
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(str(title))}</title>
<style>
:root {{ color-scheme: light; --ink:#172033; --muted:#64748b; --line:#e2e8f0; --panel:#f8fafc; --accent:#3157d5; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#f1f5f9; color:var(--ink); font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ max-width:1000px; margin:36px auto; padding:0 20px 48px; }}
header, section {{ background:white; border:1px solid var(--line); border-radius:18px; padding:26px; margin-bottom:18px; box-shadow:0 8px 24px #0f172a0a; }}
.eyebrow {{ color:var(--accent); font-size:12px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; }}
h1 {{ margin:6px 0; font-size:clamp(28px,5vw,40px); line-height:1.15; }}
h2 {{ margin:0 0 16px; font-size:21px; }}
.meta {{ color:var(--muted); overflow-wrap:anywhere; }}
.notice {{ margin-top:18px; padding:14px 16px; border-radius:12px; background:#eff6ff; color:#1e3a8a; }}
table {{ width:100%; border-collapse:collapse; }}
th,td {{ padding:12px 14px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; overflow-wrap:anywhere; }}
th {{ width:34%; color:#475569; font-weight:600; }}
tr:last-child th,tr:last-child td {{ border-bottom:0; }}
.group {{ width:auto; background:var(--panel); color:var(--ink); }}
.gallery {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }}
figure {{ margin:0; border:1px solid var(--line); border-radius:12px; overflow:hidden; background:var(--panel); }}
figure img {{ display:block; width:100%; max-height:320px; object-fit:contain; background:#e2e8f0; }}
figcaption {{ padding:10px 12px; color:#475569; font-weight:600; }}
footer {{ color:var(--muted); text-align:center; font-size:12px; padding:12px; }}
@media(max-width:600px) {{ main {{ margin:16px auto; padding:0 12px 28px; }} header,section {{ padding:18px; }} th,td {{ padding:9px 7px; }} th {{ width:42%; }} }}
@media print {{ body {{ background:white; }} main {{ margin:0 auto; }} header,section {{ box-shadow:none; break-inside:avoid; }} }}
</style>
</head>
<body>
<main>
<header>
<div class="eyebrow">TRACE-X · Image Forensics</div>
<h1>{html.escape(str(title))}</h1>
<div class="meta">Image: {html.escape(str(source))}</div>
<div class="meta">Report generated: {html.escape(str(created))}</div>
<div class="notice"><strong>How to read this report:</strong> These outputs show forensic signals and unusual patterns.
They are indicators for further review, not proof that an image was manipulated or authentic.</div>
</header>
<section><h2>Analysis summary</h2>{body}</section>
{images_section}
<footer>Generated by TRACE-X · Forensic analysis should be interpreted alongside the original image and other evidence.</footer>
</main>
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a TRACE-X JSON report into a readable HTML report.")
    parser.add_argument("json_report", type=Path, help="Path to the generated report.json")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Optional HTML output path")
    args = parser.parse_args()
    result = build_report(args.json_report, args.output)
    print(f"Readable report created: {result}")


if __name__ == "__main__":
    main()
