# Collaboration Workflow

This project is intended to be developed through GitHub pull requests. The repository owner/admin reviews and merges changes into `main`; collaborators should work from short-lived branches and keep each handoff easy to audit.

## Roles And Access

- Admin: manages repository settings, protected branches, deployment secrets, merge policy, and final PR merges.
- Collaborator: creates branches, commits focused changes, opens pull requests, responds to review comments, and keeps the local branch current with `main`.
- Both: agree on issue scope before coding, document assumptions, and avoid committing unrelated local changes.

## Branch Rules

- Do not commit directly to `main`.
- Start every task from the latest `main`:

```bash
git switch main
git pull origin main
git switch -c <type>/<short-task-name>
```

- Recommended branch prefixes:

```text
feature/...
fix/...
docs/...
test/...
chore/...
```

- Keep branches small enough to review in one sitting. If a task grows, split it into follow-up branches.

## Daily Handoff

Use this checklist before ending each work session:

- Pull the latest `main` before starting new work.
- Run the relevant verification commands.
- Commit only the files related to the task.
- Push the task branch to GitHub.
- Open or update the pull request with status, test evidence, and known gaps.
- Leave a short handoff note in the PR or project chat.

Suggested handoff note:

```text
Branch:
Scope:
What changed:
Verification:
Known issues:
Next suggested step:
```

## Pull Request Expectations

Each PR should include:

- Problem or task summary.
- Key files changed.
- Screenshots or local URL for frontend changes when useful.
- Verification commands and results.
- Any generated outputs that changed intentionally.

Before requesting review:

```bash
python -m src.reporting.generate_report
pytest
cd web
npm install
npm run build
```

For frontend-only edits, `npm run build` may be enough, but run the Python pipeline too if dashboard data or public JSON files changed.

## Local Full-Chain Run

From the repository root:

```bash
python -m pip install -e .
python -m src.reporting.generate_report
pytest
cd web
npm install
npm run build
npm run dev
```

The local dashboard runs at:

```text
http://127.0.0.1:5173/
```

## Generated Files

The Python pipeline refreshes data, metrics, charts, and report artifacts under:

```text
data/
outputs/
web/public/
```

Commit generated files only when they are part of the intended result. If generated files changed unexpectedly, inspect the diff before committing.

## Conflict Handling

- If both collaborators touch the same file, prefer syncing early through a draft PR.
- Rebase or merge from `main` before asking for final review if the branch is stale.
- Resolve conflicts locally, rerun verification, and mention the conflict resolution in the PR.

## Deployment Notes

- The React app lives in `web`.
- Vercel settings should use:

```text
Root directory: web
Framework preset: Vite
Install command: npm install
Build command: npm run build
Output directory: dist
```

- Deployment configuration is documented in `docs/deployment.md`.

## Git Hygiene

- Use clear commit messages, for example `docs: add collaboration workflow`.
- Avoid committing local environment files, caches, virtual environments, `web/node_modules`, or `web/dist`.
- Review `git status` and `git diff` before every commit.
- When in doubt, open a draft PR early and ask for review before expanding the change.
