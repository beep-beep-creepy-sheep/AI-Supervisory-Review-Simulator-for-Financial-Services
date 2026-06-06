# Deployment

This project is designed as a static React portfolio website backed by JSON files in `web/public/data`. It does not require a backend, paid APIs, or runtime secrets.

## Primary Target: Vercel

Recommended Vercel settings:

- Framework preset: Vite
- Root directory: `web`
- Install command: `npm install`
- Build command: `npm run build`
- Output directory: `dist`

Steps:

1. Push the repository to GitHub.
2. In Vercel, import the repository.
3. Set the root directory to `web`.
4. Confirm build command `npm run build`.
5. Confirm output directory `dist`.
6. Deploy.

The repository also includes `vercel.json` files for root-level and `web`-root deployment workflows.

## Netlify

Recommended Netlify settings:

- Base directory: `web`
- Build command: `npm run build`
- Publish directory: `web/dist` if deploying from repo root, or `dist` if base directory is `web`

Steps:

1. Import the GitHub repository into Netlify.
2. Set base directory to `web`.
3. Set build command to `npm run build`.
4. Set publish directory to `dist`.
5. Deploy.

## GitHub Pages

This site uses section anchors rather than React Router path routing, so GitHub Pages does not require `HashRouter` or a `basename`.

One simple approach:

```bash
cd web
npm install
npm run build
```

Then publish `web/dist` using your preferred GitHub Pages workflow.

If you later add React Router with browser history routes, use `HashRouter` or configure a fallback to `index.html` for GitHub Pages.

## Refreshing Static Data

Run the Python evaluation pipeline before deploying when you want fresh metrics:

```bash
python3 -m src.reporting.generate_report
```

This writes deployment data into:

- `web/public/data/system_inventory.json`
- `web/public/data/key_metrics.json`
- `web/public/data/risk_register.json`
- `web/public/data/genai_eval_results.json`
- `web/public/data/agentic_eval_results.json`
- `web/public/data/credit_model_metrics.json`
- `web/public/data/failure_examples.json`

## GitHub Repository Website Field

After deployment, copy the Vercel, Netlify, or GitHub Pages URL and paste it into the repository **About** section under **Website**. This makes the public demo one click away for recruiters and hiring managers.

