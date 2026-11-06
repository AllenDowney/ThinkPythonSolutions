# Google Drive + Forms + Slides Workflow

This document explains how to upload figure batches to Google Drive, keep a
matching local folder structure, generate Google Slides from those images, and
optionally create Google Forms that embed the images.

## Prerequisites

1. Enable APIs in the Google Cloud project:
   - Google Drive API
   - Google Slides API
   - Google Forms API (only needed if creating SME forms)
2. Place `credentials.json` in `sklearn/`.
3. Authenticate once to create `token.pickle`:

```bash
conda activate minerva
cd /home/downey/minerva/sklearn
python scripts/test_google_auth.py
```

## Folder Structure (Local + Drive)

Local structure is mirrored on Drive:

- Local: `minerva_figs/<set-name>/`
- Drive: `minerva_figs/<set-name>/`

The scripts create the Drive folder automatically if it does not exist and
upload each batch into the matching subfolder.

## Upload Images to Drive

Use `upload_images_to_drive.py` to upload a batch and produce a CSV of shareable
URLs (saved next to the images locally).

```bash
conda activate minerva
cd /home/downey/minerva/sklearn
python scripts/upload_images_to_drive.py \
  --image-dir /home/downey/minerva/minerva_figs/example_day \
  --pattern "example_day_*" \
  --set-name example_day
```

Outputs:
- Local CSV: `minerva_figs/example_day/image_urls.csv`
- Drive folder: `minerva_figs/example_day/`

Optional arguments:
- `--drive-root-name` (default: `minerva_figs`)
- `--drive-subfolder-name` (default: `--set-name`)
- `--output` to override CSV output path

## Create Slides from Existing URLs

Use `create_slides.py` with `--input-csv` to create slides without re-uploading.
The presentation is moved into the same Drive folder as the figures.

```bash
conda activate minerva
cd /home/downey/minerva/sklearn
python scripts/create_slides.py \
  --input-csv /home/downey/minerva/minerva_figs/example_day/image_urls.csv \
  --set-name example_day
```

Outputs:
- Slides info JSON: `minerva_figs/example_day/slides_info.json`
- Google Slides presentation stored in Drive folder `minerva_figs/example_day/`

## Optional: Upload + Create Slides in One Step

If you want to upload images and create slides in one command, omit `--input-csv`.

```bash
conda activate minerva
cd /home/downey/minerva/sklearn
python scripts/create_slides.py \
  --image-dir /home/downey/minerva/minerva_figs/example_day \
  --pattern "example_day_*" \
  --set-name example_day
```

## Create Google Forms from Image URLs

Use `create_sme_form.py` to generate a Google Form from the URL CSV. The CSV
must include `filename` and `image_url` columns. To create a quiz with correct
answers, add a `correct_answer` column and pass `--quiz`.

```bash
conda activate minerva
cd /home/downey/minerva/sklearn
python scripts/create_sme_form.py \
  --input /home/downey/minerva/minerva_figs/example_day/image_urls.csv
```

Outputs:
- Form metadata JSON: `tables/sme_form_info.json`
- Edit + responder URLs printed to the console

Quiz mode:

```bash
python scripts/create_sme_form.py \
  --input /home/downey/minerva/minerva_figs/example_day/image_urls.csv \
  --quiz \
  --points 1 \
  --answer-column correct_answer
```

Valid `correct_answer` values:
- `Yes - will have overnight low`
- `No - will not have overnight low`
- `Unsure/Ambiguous`
You can also use `yes`, `no`, or `unsure` (case-insensitive).

