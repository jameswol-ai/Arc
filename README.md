# Arc — demo web app

This branch (web-app) contains a simple static single-page demo site (HTML/CSS/JS).

Files added:

- index.html — the site
- styles.css — basic responsive styles
- script.js — small interactive behaviors (theme toggle, fetch repo info, contact form demo)
- .github/workflows/deploy-pages.yml — GitHub Actions workflow to publish to GitHub Pages from this branch

How to use

1. The files are on the `web-app` branch. You can open a PR to merge them into your default branch, or publish directly from the `web-app` branch.
2. Pages deployment: the workflow will run on pushes to `web-app` and attempt to upload the repository contents to GitHub Pages. After the workflow runs, configure GitHub Pages in repository settings to publish from "GitHub Actions" if required.

Notes

- The contact form is purely client-side and does not send messages to a server.
- The demo fetches public repository info using the GitHub API; large requests may be rate-limited for unauthenticated requests.

arc_app/
├── app.py              # Main dashboard (Central Hub)
├── pages/
│   ├── 01_Sai_Engine.py # Architectural & Structural Lab
│   └── 02_Random_FX.py  # Forex Intelligence & Hedging
└── assets/             # Optional: place CSS or local files here
