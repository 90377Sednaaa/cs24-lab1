# CS24/L — Web Application Testing Lab: OWASP Juice Shop

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Alteyae/cs24-lab1)

> **Students — how to join this lab:**
> 1. Click **Fork** (top right) to copy this repo to your own GitHub account.
> 2. On *your fork*, click the **Open in GitHub Codespaces** badge above (or
>    **Code → Codespaces → Create codespace on main**).
> 3. Wait ~1–2 minutes. Juice Shop starts automatically and a preview of it opens
>    on **port 3000**. If the preview is blank, wait ~30–60s and refresh.
> 4. Do the lab (Section 5), fill in `findings.csv`, add screenshots, and push.
>    The auto-grader (Section 8) checks your submission on every push.

**Course:** CS24/L — AI-Driven Ethical Hacking and Penetration Testing

**Coverage:** Weeks 4–5 — Web Application Testing (input fields, injection points,
client-side issues, access control, misconfigurations)

**Course Outcome:** CO1 / CO2 — perform web application security testing and analyze
vulnerabilities in a controlled, authorized environment.

**Format:** Hands-on, auto-graded via GitHub. You exploit the app, document four
findings, and push your work for automatic structural grading.

> ⚠️ **Authorized training only.** OWASP Juice Shop is intentionally vulnerable and
> please run **only on your own machine / Codespace / Virtual Machine**. Never point these techniques at a
> system you do not own or lack written permission to test.

---

## 1. Overview

OWASP **Juice Shop** is a deliberately insecure web application. In this lab you
will find and document **four** real vulnerabilities: two **SQL injection** flaws
and two **cross-site scripting (XSS)** flaws. For each, you record evidence and map
it to industry references, then push your findings to GitHub where an automated
checker validates your submission.

You are assessed on **doing the testing**, **documenting findings accurately**, and
**presenting results clearly** — the same three pillars as the course's lab exams.

---

## 2. Objectives

By the end of this lab you can:
- Launch and explore a target web application and find its testing surface.
- Discover and exploit **SQL injection** in a login form and a search endpoint.
- Discover and exploit **reflected** and **stored XSS**.
- Document findings with evidence, severity, and remediation.
- Map findings to **OWASP Top 10** and **MITRE ATT&CK**.

---

## 3. Prerequisites

- A GitHub account (to fork this repo and get auto-graded).
- **Either** GitHub Codespaces (runs in your browser) **or** Docker Desktop locally.
- A browser with DevTools (Chrome/Edge/Firefox).
- Basic familiarity with the course's web-testing topics (Weeks 4–5).

---

## 4. Setup — launch the target (step by step)

### Where does Juice Shop come from?
Juice Shop's code is **not** inside this repository. This repo only holds the lab
(instructions, template, grader) plus a `docker-compose.yml`. That file points at
the official Juice Shop image on Docker Hub:

```yaml
image: bkimminich/juice-shop:v17.1.1
```

When you run `docker compose up -d`, Docker **downloads that image** (the first run
takes a few minutes) and starts Juice Shop for you on **port 3000**. You never have
to install Juice Shop by hand — Docker does it. Pick **Path A** (browser, nothing to
install) or **Path B** (your own computer).

---

### Path A — GitHub Codespaces (easiest, runs in your browser)

**Step 1 — Fork this repo.**
Open the repo on GitHub, click **Fork** (top right), and create the fork under your
own account.

**Step 2 — Open a Codespace.**
On *your fork*, click the green **Code** button → **Codespaces** tab →
**Create codespace on main**. Wait ~1 minute for it to load (it opens a VS Code
editor in your browser — Docker is already installed inside it).

**Step 3 — Start Juice Shop.**
In the Codespace terminal (bottom panel), type:
```bash
docker compose up -d
```
Docker pulls the Juice Shop image and starts it. Wait until it prints that the
container started.

**Step 4 — Wait for it to boot, then confirm it's up.**
Give it ~30–60 seconds, then run:
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000
```
`200` means Juice Shop is running.

**Step 5 — Open it in the browser.**
Click the **Ports** tab (next to the terminal). Find port **3000**, right-click it →
**Port Visibility → Public**, then click the 🌐 globe/open icon to open the
forwarded URL. The Juice Shop homepage should appear.

**Step 6 — You're ready.** Go to Section 5 and start testing.

---

### Path B — Docker on your own computer

**Step 1 — Install Docker Desktop.**
Download and install **Docker Desktop** (docker.com), then **launch it** and wait
until it says *Docker is running*. Confirm in a terminal:
```bash
docker --version
```

**Step 2 — Get this repo onto your computer.**
Fork it on GitHub first, then clone *your fork* (replace `<your-username>`):
```bash
git clone https://github.com/<your-username>/cs24-lab1.git
cd cs24-lab1
```

**Step 3 — Start Juice Shop.**
```bash
docker compose up -d
```
The first run downloads the image (a few minutes). Later runs are instant.

**Step 4 — Wait, then confirm it's up.**
Give it ~30–60 seconds, then:
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000
```
`200` means it's running. (On Windows without `curl`, just open the URL in Step 5.)

**Step 5 — Open it in your browser.**
Go to **http://localhost:3000** — you should see Juice Shop.

**Step 6 — You're ready.** Go to Section 5 and start testing.

---

### Stopping and restarting the target
- **Stop it** (when you're done for the day): `docker compose down`
- **Start it again** next time: `docker compose up -d`
- **See logs** if something looks wrong: `docker compose logs`

> **Codespaces note:** a Codespace pauses when you close it and resumes where you
> left off. If Juice Shop isn't responding after you reopen a Codespace, just run
> `docker compose up -d` again.

---

## 5. Procedure

Work through the four findings. Keep a **screenshot** of each exploit working — you
will need them as evidence.

### Finding JUICE-001 — SQL Injection (login bypass)
- **Where:** the Login form (`/#/login`), which calls `POST /rest/user/login`.
- **Goal:** log in as the administrator **without knowing the password** by
  injecting SQL into the email field.
- **Hint:** think about what `' OR 1=1 --` style input does to a query built by
  string concatenation. Try it in the email field.
- **Evidence:** screenshot of being logged in as admin (or the admin account shown).

### Finding JUICE-002 — SQL Injection (data extraction via search)
- **Where:** the product search (`GET /rest/products/search?q=`).
- **Goal:** use a **UNION-based** injection to pull data that shouldn't appear in a
  product search (e.g. user records).
- **Hint:** close the intended query and append your own `UNION SELECT ...`.
- **Evidence:** screenshot of the injected response returning unintended data.

### Finding JUICE-003 — Reflected XSS
- **Where:** a field whose value is reflected back into the page (e.g. search).
- **Goal:** get the app to execute your injected script in the browser.
- **Hint:** a classic `<iframe src="javascript:alert(...)">` or similar payload.
- **Evidence:** screenshot of your script/alert firing.

### Finding JUICE-004 — Stored XSS
- **Where:** an input that is saved and later shown to users (e.g. a review /
  profile / feedback field).
- **Goal:** store a payload that executes when the page is viewed later.
- **Hint:** submit the payload, then reload the page that displays it.
- **Evidence:** screenshot of the stored payload executing on page load.

> **Score Board tip:** Juice Shop has a hidden **Score Board** that lists its
> challenges. Finding it is itself part of the recon. It helps you confirm which
> challenges you have solved.

---

## 6. What to submit

1. **`findings.csv`** — fill in all four rows (JUICE-001 … JUICE-004). Keep the
   header row exactly as provided. Columns are described in Section 7.
2. **`screenshots/`** — one image per finding, named `JUICE-001.png` …
   `JUICE-004.png` (`.png` or `.jpg`).
3. **`attacker_scripts/`** *(optional but encouraged)* — any scripts/payloads you
   used, so your work is reproducible.
4. **Commit and push** to your fork. The GitHub Action grades your submission
   automatically (see Section 8). Check the **Actions** tab for your result.

```bash
git add findings.csv screenshots/ attacker_scripts/
git commit -m "Submit Juice Shop findings"
git push
```

---

## 7. findings.csv columns

| Column | What goes in it |
|---|---|
| `finding_id` | `JUICE-001` … `JUICE-004` (exactly). |
| `title` | Short name of the vulnerability. |
| `vuln_type` | One of: `SQL Injection`, `XSS - Reflected`, `XSS - Stored`. |
| `url_or_endpoint` | Where you found it (e.g. `/rest/user/login`). |
| `severity` | One of: `Low`, `Medium`, `High`, `Critical`. |
| `owasp` | OWASP Top 10 mapping (e.g. `A03:2021 - Injection`). |
| `mitre_attack` | A MITRE ATT&CK technique ID (e.g. `T1190`). |
| `payload_used` | The exact input/payload you submitted. |
| `impact` | What an attacker gains (1–2 sentences). |
| `remediation` | How to fix it (1–2 sentences). |
| `screenshot` | Filename in `screenshots/` (e.g. `JUICE-001.png`). |

A pre-filled skeleton with the four finding IDs is already in `findings.csv` — just
complete the empty cells.

---

## 8. Grading (100 points)

| Finding | Points |
|---|---|
| JUICE-001 — SQL Injection (login) | 25 |
| JUICE-002 — SQL Injection (search) | 25 |
| JUICE-003 — Reflected XSS | 25 |
| JUICE-004 — Stored XSS | 25 |

**Automated check (on every push)** — `tests/test_findings.py`, run by the GitHub
Action in `.github/workflows/grade.yml`, verifies that your submission is
**complete and well-formed**:
- `findings.csv` exists and has exactly the four required rows with the correct IDs.
- All required columns are present and non-empty.
- `vuln_type` and `severity` use only the allowed values.
- Each finding references a screenshot file that actually exists in `screenshots/`.

> **Important:** the auto-grader checks that your submission is **structurally
> complete** — it does **not** by itself prove you really exploited the app. Your
> **screenshots** are your proof, and your instructor spot-checks them. Inventing
> findings or screenshots is an academic-integrity violation (Section 10).

Run the same check yourself before pushing:
```bash
python -m pip install pytest
pytest -q
```

---

## 9. Troubleshooting

- **Port 3000 not showing / app not loading:** wait ~30–60s after `docker compose
  up -d` for Juice Shop to finish booting, then refresh. Check `docker compose logs`.
- **Codespace port is private:** in the **Ports** tab, right-click port 3000 →
  Port Visibility → **Public**.
- **`pytest` can't find the CSV:** run it from the repo root (where `findings.csv`
  lives).
- **Auto-grade failed:** open the **Actions** tab → the failed run → read the
  message. It names the row/column/screenshot that's missing or invalid.

---

## 10. Academic Integrity

Per the course policy on academic integrity:
- Do your own testing; do not copy another student's `findings.csv` or screenshots.
- Do not fabricate or invent findings, payloads, or evidence.
- Using an AI assistant to **explain** a vulnerability or **tidy your writing** is
  allowed; submitting AI-generated findings you did not reproduce is not.
- All testing happens only against your own local/Codespace Juice Shop instance.

---

*Prepared for CS24/L — Web Application Testing Lab. Local, authorized training use only.*
