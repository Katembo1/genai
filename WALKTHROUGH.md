# Walkthrough — genai repository

This written walkthrough demonstrates how to run a sample component from this repository and where to find generated documentation and outputs.

## Goal

Run the `frontend` Python app as a sample demonstration, and point to documentation that ships inside the repository.

## Environment

- OS: Windows
- Shell: PowerShell
- Python 3.8+

## Step-by-step (PowerShell)

1. From the repository root, create and activate a virtual environment:

```powershell
cd c:\playground2\jac
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies for the frontend and run it:

```powershell
cd frontend
pip install -r requirements.txt
python app.py
```

3. Expected behavior

- The frontend app uses `streamlit` (or plain Flask/other based app depending on implementation). When it runs, it typically opens a local web UI or prints a listening address in the console (for example, `Running on http://127.0.0.1:8501` for Streamlit). Follow that address in your browser.

4. Other components

- To run other Python components in this repository: install the component's `requirements.txt` and run that component's entrypoint (for example `python app.py`).
- Jaseci/Jac artifacts under `backend/` require the Jaseci runtime. See https://jaseci.org for details on how to run `.jac` files and the proper runtime tooling.

## Where to find documentation and generated docs

Look for `docs/` directories and component `README.md` files across the repository. Open those markdown files in your editor or on GitHub to read architecture notes, setup instructions, and examples.

## External libraries and APIs used

See the `requirements.txt` files for each component. Examples you may encounter include:

- streamlit, requests, markdown

Licensing note: each third-party package has its own license. This repository does not contain a repository-level `LICENSE` file; if you plan to redistribute or use this code in a product, add a `LICENSE` file to the repo root and verify the dependency licenses.

## Sample outputs and artifacts

- When the frontend runs you will see console logs and a http URL. That UI is the demonstration surface.
- Project docs listed above are plain markdown files. If you have a docs generator in your workflow (Sphinx, MkDocs, or similar), generated HTML may be located elsewhere — search the repo for `docs/_build` or similar.

## Video walkthrough

If you recorded a video walkthrough, add the public URL here and update the top of `README.md` with the link.

## Next steps (suggested)

- Add a repository-level `LICENSE` file (for example MIT or Apache-2.0).
- If you want, add a short recorded video and paste the link at the top of `README.md` and in the Google form.
- Add a tiny CI check that runs `python -m pip install -r frontend/requirements.txt` to ensure dependencies remain installable.

---
Written walkthrough created: 2025-11-07
