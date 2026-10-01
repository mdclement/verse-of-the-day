#!/usr/bin/env python3
"""
Gospel Library - Verse of the Day Fridge Printable Generator
Fetches the current "Verse of the Day" from churchofjesuschrist.org (the same source as the Gospel Library app)
and produces a clean, high-impact, large-print single-page printable (HTML and/or PDF) designed for the fridge.
"""

import argparse
import datetime
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.request
import webbrowser
from typing import Dict, Optional, Tuple

from bs4 import BeautifulSoup


PAGE_URL = "https://www.churchofjesuschrist.org/my-home?lang=eng"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch_page_html(url: str = PAGE_URL) -> str:
    """Fetch the raw HTML from the Church website."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        content_bytes = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        try:
            return content_bytes.decode(charset)
        except UnicodeDecodeError:
            return content_bytes.decode("utf-8", errors="replace")


def extract_verse_data(page_html: str) -> Dict[str, str]:
    """
    Extract the Verse of the Day text, scripture reference, and link from HTML.
    """
    verse_text = ""
    reference = ""
    scripture_url = ""

    soup = BeautifulSoup(page_html, "html.parser")

    votd_heading = None
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "div", "span"]):
        if tag.get_text(strip=True).lower() == "verse of the day":
            votd_heading = tag
            break

    if votd_heading:
        card = votd_heading.find_parent("div")
        if card:
            link_tag = card.find("a")
            if link_tag:
                reference = link_tag.get_text(strip=True)
                href = str(link_tag.get("href") or "")
                scripture_url = (
                    f"https://www.churchofjesuschrist.org{href}"
                    if href.startswith("/")
                    else href
                )

            text_candidates = []
            for elem in card.find_all(["div", "p", "span"]):
                text = elem.get_text(strip=True)
                if (
                    text
                    and text.lower() != "verse of the day"
                    and text != reference
                    and not elem.find("a")
                    and not elem.find(["h1", "h2", "h3", "h4", "h5", "h6"])
                ):
                    text_candidates.append(text)

            if text_candidates:
                verse_text = max(text_candidates, key=len)

    if not verse_text:
        raise ValueError("Could not find 'Verse of the Day' on the webpage. The page structure may have changed.")

    # Clean text formatting
    verse_text = re.sub(r"\s+", " ", verse_text).strip()
    reference = re.sub(r"\s+", " ", reference).strip()

    return {
        "verse": verse_text,
        "reference": reference or "Scripture",
        "url": scripture_url,
    }


def calculate_optimal_font_sizes(verse_len: int) -> Tuple[str, str, str]:
    """
    Calculate responsive font sizes so the verse occupies the page with maximum readability
    without overflowing the single-page boundary.
    Returns: (body_font_size, line_height, ref_font_size)
    """
    if verse_len < 90:
        return ("46pt", "1.45", "30pt")
    elif verse_len < 160:
        return ("40pt", "1.45", "28pt")
    elif verse_len < 260:
        return ("38pt", "1.45", "26pt")
    elif verse_len < 400:
        return ("30pt", "1.4", "24pt")
    elif verse_len < 600:
        return ("23pt", "1.4", "20pt")
    else:
        return ("16pt", "1.4", "16pt")


def generate_html_content(
    verse_data: Dict[str, str],
    auto_print: bool = False,
    landscape: bool = False,
) -> str:
    """Generate a high-quality, large-print single-page printable HTML document."""
    verse_text = html.escape(verse_data["verse"])
    reference = html.escape(verse_data["reference"])
    date_str = datetime.date.today().strftime("%A, %B %d, %Y")
    font_size, line_height, ref_font_size = calculate_optimal_font_sizes(len(verse_data["verse"]))
    page_orientation = "landscape" if landscape else "portrait"
    page_width = "11in" if landscape else "8.5in"
    page_height = "8.5in" if landscape else "11in"

    print_script = "window.addEventListener('load', () => window.print());" if auto_print else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verse of the Day - {reference}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400;1,600&display=swap');

        @page {{
            size: letter {page_orientation};
            margin: 0.5in;
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}

        body {{
            margin: 0;
            padding: 20px;
            background: #f4f6f8;
            color: #111827;
            font-family: 'Lora', Georgia, 'Times New Roman', serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }}

        .toolbar {{
            margin-bottom: 20px;
        }}

        .toolbar button {{
            background: #111827;
            color: #ffffff;
            border: none;
            padding: 10px 16px;
            font-size: 14px;
            cursor: pointer;
        }}

        .page-sheet {{
            width: {page_width};
            height: {page_height};
            max-width: 100%;
            background: #ffffff;
            padding: 0.75in;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .verse-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}

        .verse-text {{
            font-size: {font_size};
            line-height: {line_height};
            font-weight: 400;
            margin: 0;
        }}

        .reference-container {{
            margin-top: 24px;
        }}

        .reference-text {{
            font-size: {ref_font_size};
            font-weight: 600;
            margin: 0;
        }}

        .date-footer {{
            margin: 12px 0 0;
            color: #6b7280;
            font-size: 10pt;
            text-align: center;
        }}

        @media print {{
            body {{
                background: none;
                padding: 0;
                margin: 0;
            }}
            .toolbar {{
                display: none !important;
            }}
            .page-sheet {{
                width: 100%;
                height: 100vh;
                max-width: none;
                padding: 0;
                page-break-inside: avoid;
                page-break-after: avoid;
            }}
        }}
    </style>
    <script>
        {print_script}
    </script>
</head>
<body>
    <div class="toolbar">
        <button onclick="window.print()">
            Print Verse
        </button>
    </div>

    <div class="page-sheet">
        <main class="verse-container">
            <p class="verse-text">{verse_text}</p>
            <div class="reference-container">
                <p class="reference-text">{reference}</p>
            </div>
        </main>
        <p class="date-footer">{date_str}</p>
    </div>
</body>
</html>
"""


def find_browser_executable() -> Optional[str]:
    """Find a Chromium-based browser (Edge, Chrome) to render PDF in headless mode."""
    candidates = [
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        shutil.which("chromium"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def export_to_pdf(html_file_path: str, pdf_file_path: str) -> bool:
    """Generate a PDF from the HTML file using headless Edge/Chrome."""
    browser_exe = find_browser_executable()
    if not browser_exe:
        print("Note: No Chromium browser (Edge/Chrome) found for automated headless PDF export.")
        print("You can still print to PDF directly from your browser by opening the HTML file.")
        return False

    abs_html = os.path.abspath(html_file_path)
    abs_pdf = os.path.abspath(pdf_file_path)

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=2000",
        f"--print-to-pdf={abs_pdf}",
        abs_html,
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
            return True
        else:
            print(f"Browser PDF generation exited with code {res.returncode}: {res.stderr}")
            return False
    except Exception as e:
        print(f"Error running PDF generation: {e}")
        return False


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Pull the LDS Gospel Library 'Verse of the Day' and generate a large-print single-page printable."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="verse_of_the_day.html",
        help="Path for output HTML file (default: verse_of_the_day.html)",
    )
    parser.add_argument(
        "--pdf",
        nargs="?",
        const="verse_of_the_day.pdf",
        default=None,
        help="Also export directly to PDF (optional file name, default: verse_of_the_day.pdf)",
    )
    parser.add_argument(
        "--open",
        dest="open_browser",
        action="store_true",
        default=True,
        help="Open the generated printable in your default browser (default: True)",
    )
    parser.add_argument(
        "--no-open",
        dest="open_browser",
        action="store_false",
        help="Do not automatically open the generated printable in a browser",
    )
    parser.add_argument(
        "--print",
        dest="auto_print",
        action="store_true",
        default=False,
        help="Automatically trigger the print dialog when opened in the browser",
    )
    parser.add_argument(
        "--landscape",
        action="store_true",
        help="Generate the printable in landscape orientation (default: portrait)",
    )

    args = parser.parse_args()

    print("Fetching 'Verse of the Day' from churchofjesuschrist.org...")
    try:
        page_html = fetch_page_html()
        verse_data = extract_verse_data(page_html)
    except Exception as e:
        print(f"Error fetching verse: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print(f"Reference : {verse_data['reference']}")
    print(f"Verse     : {verse_data['verse']}")
    if verse_data.get("url"):
        print(f"Link      : {verse_data['url']}")
    print("=" * 60 + "\n")

    html_content = generate_html_content(
        verse_data,
        auto_print=args.auto_print,
        landscape=args.landscape,
    )
    output_html_path = os.path.abspath(args.output)

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Generated printable HTML: {output_html_path}")

    pdf_created = False
    if args.pdf:
        pdf_path = os.path.abspath(args.pdf)
        print(f"Rendering PDF with headless browser...")
        if export_to_pdf(output_html_path, pdf_path):
            print(f"[OK] Generated printable PDF: {pdf_path}")
            pdf_created = True

    if args.open_browser:
        target_to_open = os.path.abspath(args.pdf) if (args.pdf and pdf_created) else output_html_path
        print(f"Opening in browser: {target_to_open}")
        webbrowser.open(pathlib.Path(target_to_open).as_uri())


if __name__ == "__main__":
    main()
