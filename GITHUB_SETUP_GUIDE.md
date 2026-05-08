# 🛠 GitHub Setup Guide — Step by Step

This guide walks you through putting the entire project on GitHub from scratch.
Estimated time: **15–20 minutes**.

---

## Step 1 — Create the GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** button (top right) → **New repository**
3. Fill in:
   - **Repository name**: `supply-chain-analytics`
   - **Description**: `End-to-end supply chain delay analysis — India-centric trade routes, ML model, GenAI recommendations`
   - **Visibility**: Public (so your professor can view it without an account)
   - ✅ Check **"Add a README file"** — we'll replace this with our own
4. Click **Create repository**

---

## Step 2 — Install Git (if you don't have it)

```bash
# Check if Git is installed
git --version

# If not installed:
# Windows → https://git-scm.com/download/win
# Mac     → brew install git
# Linux   → sudo apt install git
```

Set your identity (one-time setup):
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## Step 3 — Set Up the Local Folder

Create the folder structure on your computer:

```
supply-chain-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
├── sql/
└── presentation/
```

**Quick way — paste this in your terminal:**
```bash
mkdir supply-chain-analytics
cd supply-chain-analytics
mkdir -p data/raw data/processed notebooks scripts sql presentation
```

---

## Step 4 — Add All Project Files

Copy these files from your downloads into the correct folders:

| File | Destination |
|------|-------------|
| `README.md` | root (`supply-chain-analytics/`) |
| `requirements.txt` | root |
| `LICENSE` | root |
| `.gitignore` | root |
| `shipment.csv` | `data/raw/` |
| `shipment_cleaned.csv` | `data/processed/` |
| `Supply_Chain_Analytics.ipynb` | `notebooks/` |
| `data_cleaning.py` | `scripts/` |
| `queries.sql` | `sql/` |
| `Supply_Chain_Analytics.pptx` | `presentation/` |

---

## Step 5 — Initialise Git and Push

```bash
# Make sure you're inside the project folder
cd supply-chain-analytics

# Initialise git
git init

# Connect to your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/supply-chain-analytics.git

# Stage all files
git add .

# First commit
git commit -m "Initial commit: full supply chain analytics project

- Phase 1: Business questions
- Phase 2: Data cleaning (24 corrupted rows identified and fixed)
- Phase 3: Feature engineering (9 new columns)
- Phase 4: EDA with 7 charts
- Phase 5: Delay probability analysis + ML model
- Phase 6: Plotly visualisations (Sankey, heatmap, world map)
- Phase 7: 6 SQL queries on SQLite
- Phase 8: GenAI recommendations via Claude API"

# Push to GitHub
git branch -M main
git push -u origin main
```

If prompted for credentials, use your GitHub username and a **Personal Access Token** (not your password):
- Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → Generate new token
- Check: `repo` scope
- Copy the token and paste it as your password

---

## Step 6 — Update the Colab Badge in README

Open `README.md` and replace `YOUR_USERNAME` with your actual GitHub username in this line:

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/supply-chain-analytics/blob/main/notebooks/Supply_Chain_Analytics.ipynb)
```

Then push the update:
```bash
git add README.md
git commit -m "docs: update Colab badge with correct GitHub username"
git push
```

---

## Step 7 — Team Collaboration (Branching Workflow)

Each member works on their own branch and merges via Pull Request:

```bash
# Member 3 working on feature engineering
git checkout -b feature/feature-engineering
# ... make changes ...
git add .
git commit -m "feat: add 9 engineered columns including is_delayed and clearance_bucket"
git push origin feature/feature-engineering
# Then open a Pull Request on GitHub → merge into main
```

**Branch naming convention:**
- `feature/data-cleaning`
- `feature/eda-charts`
- `feature/ml-model`
- `fix/customs-column-type`
- `docs/update-readme`

---

## Step 8 — Set Up GitHub Projects (Optional but Impressive)

1. Go to your repo → **Projects** tab → **New project**
2. Choose **Board** view
3. Create columns: `To Do` | `In Progress` | `Review` | `Done`
4. Add one card per phase — assign to the responsible member
5. Move cards as work progresses

This shows evaluators you ran it like a real project.

---

## Step 9 — Verify Everything Looks Good

Visit `https://github.com/YOUR_USERNAME/supply-chain-analytics` and check:

- [ ] README renders with the Colab badge
- [ ] Notebook renders in-browser (GitHub shows `.ipynb` files beautifully)
- [ ] `data/raw/shipment.csv` is present
- [ ] `data/processed/shipment_cleaned.csv` is present
- [ ] SQL file is readable in the browser
- [ ] All team members are added as **Collaborators** (Settings → Collaborators → Add people)

---

## Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| `git push` asks for password | Use a Personal Access Token, not your GitHub password |
| `.ipynb` not rendering | GitHub sometimes needs a refresh — try nbviewer.org as backup |
| File too large (>100MB) | Use Git LFS: `git lfs track "*.csv"` then commit |
| Wrong remote URL | `git remote set-url origin https://github.com/CORRECT_USER/supply-chain-analytics.git` |
| Merge conflict | `git pull origin main` before pushing; resolve conflicts, then push |

---

*Questions? Raise a GitHub Issue on the repo — that's how real teams communicate.*
