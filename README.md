 # genai

This repository contains the genai demo project composed of several components (backend jac artifacts and Python frontends). This README explains how to run the main pieces, where to find generated documentation in the repo, and lists external dependencies and licensing notes.

Repository (public): https://github.com/Katembo1/genai (branch: main)

## Quick overview

- Backend: jac artifacts under `backend/`.
- Python frontends: `frontend/app.py`.
- Documentation: search the repository for `docs/` directories or open component README files for component-specific documentation.

## Where generated documentation lives

The repository may include project documentation inside component folders (look for `docs/` directories). Open component README or docs files for architecture details and setup steps.

## Prerequisites

- Python 3.8+ (for Python apps)
- pip
- (Optional) Jaseci/Jac runtime to run `.jac` files and Jaseci artifacts.

If you plan to run the jac files you will need the Jaseci runtime — see https://jaseci.org for installation instructions.

## Install and run (example: frontend)

Below are sample steps for running the `frontend` app on Windows PowerShell.

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install the frontend dependencies and run the app:

```powershell
cd frontend
pip install -r requirements.txt
python app.py
```

Repeat similar steps for other Python apps in the repository by installing the app-specific `requirements.txt` and running the app's entrypoint (for example, `python app.py`).

For jac back-end components in `backend/` refer to the Jaseci documentation to run `.jac` programs.

## Generated documentation and walkthrough

- This repository includes a written walkthrough in `WALKTHROUGH.md` that demonstrates running a sample component and where to find outputs and docs.
- If you have a hosted video walkthrough, link it here. (Add video URL when available.)

## External libraries / APIs used

Key Python dependencies can be found in each component's `requirements.txt` file. Examples from the repo include:

- `frontend/requirements.txt`: streamlit, requests, markdown
- `backend/requirements.txt`: (see `backend/requirements.txt` in the repo)

Important: These packages have their own licenses (MIT, Apache-2.0, or others). Before using or redistributing, verify each package's license. No repository-level `LICENSE` file was found in this repo — consider adding an explicit license to this repository to make reuse and redistribution terms clear.

## Licensing considerations

- Check the licenses for third-party libraries listed above before redistribution or commercial use.
- If you want this repository to be explicitly licensed, add a `LICENSE` file (for example, `MIT` or `Apache-2.0`) to the repository root.

## Walkthrough and demo

See `WALKTHROUGH.md` for a written walkthrough demonstrating how to run a sample repository component and where to find generated documentation and outputs.

## Contact / Video

If you provided a video walkthrough in the Google form or elsewhere, add the public link here.

---
Last updated: 2025-11-07
