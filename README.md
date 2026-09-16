# LDS Gospel Library - Verse of the Day Printable

A Python script that scrapes the current **Verse of the Day** from [churchofjesuschrist.org](https://www.churchofjesuschrist.org/my-home?lang=eng) (the same feed displayed on the Gospel Library home screen) and generates an elegant, large-print, single-page printable sheet designed for your refrigerator or display board.

---

## Features

- **Live Scraper**: Pulls the daily verse and scripture reference directly from the Church website.
- **Large Print Single-Page Layout**: Formatted for standard US Letter (8.5" × 11") portrait printing with dynamic font scaling (scales text up for short verses and adjusts for longer verses so it always fits on a single page).
- **Elegant Aesthetic**: Framed border, refined typography (Cinzel & Lora serif fonts), quotation marks, and date header.
- **PDF & HTML Export**: Generates an HTML file and can automatically compile a clean PDF using headless Microsoft Edge or Google Chrome without third-party binary dependencies.
- **Quick Print**: Includes a browser print button and opens automatically for immediate one-click printing.

---

## Installation

1. Install Python 3.8+ (if not already installed).
2. Install the required dependency:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Basic Run (HTML + Open in Browser)
Runs the script, displays the verse in the console, generates `verse_of_the_day.html`, and opens it in your default browser:

```bash
python verse_of_the_day.py
```

Click **Print Verse** at the top or press `Ctrl + P` to print.

---

### 2. Export Directly to PDF
Generate both the HTML and a ready-to-print `verse_of_the_day.pdf`:

```bash
python verse_of_the_day.py --pdf
```

Specify a custom PDF path:
```bash
python verse_of_the_day.py --pdf my_daily_verse.pdf
```

---

### 3. Open Directly with Print Dialog Triggered

```bash
python verse_of_the_day.py --print
```

### 4. Generate in Landscape Orientation

Portrait is the default. Add `--landscape` for a letter-sized landscape printable:

```bash
python verse_of_the_day.py --landscape
```

---

### 5. Command Line Options

| Option | Description | Default |
|---|---|---|
| `-o`, `--output` | Output HTML filename | `verse_of_the_day.html` |
| `--pdf [FILENAME]` | Export to PDF using headless Edge/Chrome | None (`verse_of_the_day.pdf` if flag provided without name) |
| `--no-open` | Do not open in browser automatically | False |
| `--print` | Auto-trigger browser print dialog on load | False |
| `--landscape` | Generate the printable in landscape orientation | False |

---

## Printing Tips for the Fridge

- In your browser print dialog (`Ctrl + P`):
  - **Destination**: Choose your printer or "Save as PDF"
  - **Layout**: Portrait
  - **Paper Size**: Letter (8.5" × 11")
  - **Margins**: Set to **Default** or **None**
  - **Headers and Footers**: Uncheck (the template has built-in headers and footers)
  - **Background graphics**: Check (to print the frame shading)
