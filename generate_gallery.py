import argparse
import base64
import json
import os

IMG_WIDTH = 3250
IMG_HEIGHT = 2500

NAV_TOP = 5
NAV_LEFT = 5
PAGINATION_BOTTOM = 3
PAGINATION_RIGHT = 3

OUTPUT_DIR = "generated_galleries"

FIGURES = [
    {
        "filename": "figures/Indicator-1.png",
        "label": "Extreme structure or properties",
        "color": "#73B5E3",
        "bg_color": "#DFF1FD",
    },
    {
        "filename": "figures/Indicator-2.png",
        "label": "Novel discrete function",
        "color": "#6FBCAD",
        "bg_color": "#E0F5F1",
    },
    {
        "filename": "figures/Indicator-3.png",
        "label": "Conservation or convergence of function",
        "color": "#FFB883",
        "bg_color": "#FFF0E0",
    },
]

HTML_HEADER = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>perspective-search-strategy-bio-utility figure gallery</title>

    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />

    <style>
        body, html {{ 
            margin: 0; padding: 0; width: 100%; height: 100%; 
            overflow: hidden; 
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .figure-wrapper {{
            position: relative;
            aspect-ratio: {IMG_WIDTH} / {IMG_HEIGHT};
            width: min(100vw, 100vh * ({IMG_WIDTH} / {IMG_HEIGHT}));
            margin-inline: auto;
            container-type: inline-size;
        }}

        .image-layer {{ 
            position: absolute; top: 0; left: 0; 
            width: 100%; height: 100%; 
            object-fit: fill; 
            opacity: 0; transition: opacity 0.4s ease-in-out; 
            pointer-events: none; z-index: 1; 
        }}
        .image-layer.active {{ opacity: 1; z-index: 2; }}

        .nav-wrapper {{
            position: absolute;
            top: {NAV_TOP}%;
            left: {NAV_LEFT}%;
            z-index: 100;
            font-size: clamp(8px, 2cqi, 32px);
            display: flex;
            align-items: center;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.08));
            cursor: pointer;
            transition: transform 0.2s ease;
        }}

        .pagination-wrapper::before {{
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: calc(100% - 4px); height: calc(100% - 4px);
            border-radius: 999px;
            z-index: -1;
            box-shadow: 0 0 0 0 rgba(0,0,0,0.1);
            animation: pulse-shadow 3s infinite;
            opacity: 1;
            transition: opacity 0.5s;
        }}

        @keyframes pulse-shadow {{
            0% {{ box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.1); }}
            70% {{ box-shadow: 0 0 0 1em rgba(0, 0, 0, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }}
        }}

        .pagination-wrapper {{
            position: absolute;
            bottom: {PAGINATION_BOTTOM}%;
            right: {PAGINATION_RIGHT}%;
            z-index: 100;
            font-size: clamp(10px, 2cqi, 24px);
            display: flex;
            align-items: center;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.08));
        }}

        .nav-wrapper:hover {{
            filter: drop-shadow(0 8px 16px rgba(0,0,0,0.12));
        }}

        .indicator-pill, .pagination-pill {{
            background-color: #FFFFFF;
            border-radius: 999px;
            padding: 0.75em 1.3em; 
            display: flex;
            align-items: center;
            gap: 0.5em;
            color: #555;
            font-weight: 600;
            position: relative;
            z-index: 10; 
        }}

        .pagination-pill {{
            gap: 0.8em;
            padding: 0.5em 0.8em;
        }}

        .number-circle {{
            background-color: var(--active-color);
            color: white;
            width: 1.6em;
            height: 1.6em;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.9em;
            line-height: 1;
            transition: background-color 0.3s ease;
        }}

        .label-pill {{
            background-color: var(--active-bg);
            border-radius: 999px; 
            margin-left: -2.2em; 
            padding: 0.75em 1.6em 0.75em 2.8em; 
            display: flex;
            align-items: center;
            gap: 0.8em;
            color: #111;
            font-weight: 500;
            position: relative;
            z-index: 5;
            transition: background-color 0.3s ease;
        }}

        .nav-btn {{
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background 0.2s, color 0.2s;
            color: #444;
            user-select: none;
            width: 1.8em;
            height: 1.8em;
        }}

        .nav-btn:hover {{
            background-color: #f0f0f0;
            color: #000;
        }}

        .material-symbols-rounded {{
            font-size: 1.4em;
            font-variation-settings: 'FILL' 0, 'wght' 500, 'GRAD' 0, 'opsz' 24;
        }}

        .dropdown-arrow {{
            width: 1.0em;
            height: 1.0em;
            opacity: 0.6;
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        }}

        .nav-wrapper.is-open .dropdown-arrow {{
            transform: rotate(180deg);
        }}

        .dropdown-menu {{
            position: absolute;
            top: 130%; 
            left: 0;
            min-width: 100%;
            width: max-content;
            background: white;
            border-radius: 0.8em;
            padding: 0.4em;
            opacity: 0;
            transform: translateY(-10px);
            pointer-events: none;
            transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
            display: flex;
            flex-direction: column;
            gap: 0.1em;
            z-index: 200;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}

        .nav-wrapper.is-open .dropdown-menu {{
            opacity: 1;
            transform: translateY(0);
            pointer-events: auto;
        }}

        .menu-item {{
            padding: 0.6em 1em; 
            border-radius: 0.5em;
            cursor: pointer;
            font-size: 0.85em;
            color: #444;
            display: flex;
            align-items: center;
            gap: 0.8em;
            transition: background 0.1s;
            white-space: nowrap;
        }}

        .menu-item:hover {{
            background-color: #F7F7F7;
            color: #000;
        }}

        .menu-dot {{
            width: 0.6em; 
            height: 0.6em; 
            border-radius: 50%;
            background-color: var(--item-color);
            flex-shrink: 0;
        }}

    </style>
</head>
<body>

<div class="figure-wrapper">

    <div class="nav-wrapper" id="navWrapper" onclick="toggleMenu(event)">
        <div class="indicator-pill">
            <span>Indicator</span>
            <div class="number-circle" id="indicatorNum">1</div>
        </div>
        <div class="label-pill">
            <span id="currentLabel">Loading...</span>
            <svg class="dropdown-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
        </div>
        <div class="dropdown-menu">
"""

HTML_JS_TEMPLATE = """        </div>
    </div>

    <div class="pagination-wrapper">
        <div class="pagination-pill">
            <div class="nav-btn" onclick="prevImage(event)" title="Previous">
                <span class="material-symbols-rounded">chevron_left</span>
            </div>
            <div class="nav-btn" onclick="nextImage(event)" title="Next">
                <span class="material-symbols-rounded">chevron_right</span>
            </div>
        </div>
    </div>

    {img_tags}

</div>

<script>
    const FIGURES = {json_data};

    let currentIndex = 0;
    const navWrapper = document.getElementById('navWrapper');
    const indicatorNum = document.getElementById('indicatorNum');
    const currentLabel = document.getElementById('currentLabel');
    const imageLayers = document.querySelectorAll('.image-layer');

    function init() {{
        updateUI(0);

        document.addEventListener('click', (e) => {{
            if (!navWrapper.contains(e.target)) {{
                navWrapper.classList.remove('is-open');
            }}
        }});

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight') nextImage(e);
            if (e.key === 'ArrowLeft') prevImage(e);
        }});
    }}

    function toggleMenu(event) {{
        event.stopPropagation();
        navWrapper.classList.toggle('is-open');
    }}

    function selectItem(event, index) {{
        event.stopPropagation();
        currentIndex = index;
        updateUI(index);
        navWrapper.classList.remove('is-open');
    }}

    function nextImage(event) {{
        if (event) event.stopPropagation();
        currentIndex = (currentIndex + 1) % FIGURES.length;
        updateUI(currentIndex);
    }}

    function prevImage(event) {{
        if (event) event.stopPropagation();
        currentIndex = (currentIndex - 1 + FIGURES.length) % FIGURES.length;
        updateUI(currentIndex);
    }}

    function updateUI(index) {{
        const fig = FIGURES[index];

        navWrapper.style.setProperty('--active-color', fig.color);
        navWrapper.style.setProperty('--active-bg', fig.bg_color);

        indicatorNum.textContent = index + 1;
        currentLabel.textContent = fig.label;

        imageLayers.forEach((img, i) => {{
            if (i === index) img.classList.add('active');
            else img.classList.remove('active');
        }});
    }}

    init();
</script>
</body>
</html>
"""


def generate(output_filename):
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    img_buffer = ""
    menu_buffer = ""
    json_data = []

    for fig in FIGURES:
        f_path = fig["filename"]

        mime_type = "image/png"

        with open(f_path, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode("utf-8")
            json_data.append(fig)
            img_buffer += f'<img src="data:{mime_type};base64,{b64}" class="image-layer" alt="{fig["label"]}">'

    for i, fig in enumerate(FIGURES):
        menu_buffer += f"""
            <div class="menu-item" onclick="selectItem(event, {i})" style="--item-color: {fig["color"]}">
                <div class="menu-dot"></div>
                <strong>Indicator {i + 1}</strong>&nbsp;{fig["label"]}
            </div>
        """

    final_html = (
        HTML_HEADER
        + menu_buffer
        + HTML_JS_TEMPLATE.format(img_tags=img_buffer, json_data=json.dumps(json_data))
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Success! Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Recreate figure gallery for the Arcadia Science pub, Strategizing the search for bio-utility: Establishing a framework for evolution-integrated in silico bioprospecting."
    )
    parser.add_argument(
        "filename",
        help="Output filename (e.g., gallery.html)",
    )
    args = parser.parse_args()

    generate(args.filename)


if __name__ == "__main__":
    main()
