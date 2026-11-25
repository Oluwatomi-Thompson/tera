# Tera

Tera is a localized investment-literacy platform for Rwandan youth. It provides learning content and tools intended to help users build practical financial knowledge.

> **Live application:** [Add your deployed application URL here](https://your-live-app-url.example)  
> Replace the example URL above with the real public URL before submitting.

## Project documents

- [Software Requirements Specification (SRS)](docs/srs/Oluwatomi_Thompson_Assignment2_10262026.pdf)
- [Architecture and system design](docs/architecture/)
- [Design/prototype materials](docs/figma/)
- [Research and supporting information](docs/research/)

## Main capabilities

The application is organized around these areas:

- User registration, sign-in, and account access
- Investment-literacy lessons and quizzes
- Learning progress tracking
- Information about relevant financial institutions
- An administrator area for managing application content and related data

Refer to the SRS and system-design materials above for the authoritative requirements and intended user flows.

## Technology

- Python and Flask
- Flask-SQLAlchemy and Flask-Migrate
- SQLite for local development; PostgreSQL is supported for deployment
- Tailwind CSS, built with Node.js and npm

## Run locally

### Prerequisites

Install:

- Git
- Python 3.12 or newer
- Node.js and npm

### 1. Clone the repository and enter the project directory

```bash
git clone https://github.com/Oluwatomi-Thompson/tera.git
cd tera
```

### 2. Create and activate a Python virtual environment

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install JavaScript dependencies and build the styles

```bash
npm ci
npm run build-css
```

To rebuild the CSS automatically while editing templates or styles, run `npm run watch-css` in a separate terminal and leave it running.

### 5. Configure local environment variables

Copy the example environment file:

**macOS/Linux:**

```bash
cp .env.example .env
```

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

The example configures Flask and a local SQLite database. Set `SECRET_KEY` in `.env` to a new, private value for your local environment. Do not commit `.env` or share its secrets. The development configuration will use a local SQLite database if `DATABASE_URL` is not set.

### 6. Create/update the database and load the starter content

With the virtual environment active and from the repository root, run:

```bash
flask db upgrade
flask seed-db
```

The seed command loads lesson and institution data from the project content files. It is safe to run again after updating those files.

### 7. (Optional) Create an administrator account

To use administrator-only screens locally, create an admin account:

```bash
flask create-admin --email you@example.com
```

The command will prompt you to enter and confirm a password. Do not put real passwords in this README or commit them to the repository.

### 8. Start the development server

```bash
flask run
```

Open <http://127.0.0.1:5000> in your browser. Press `Ctrl+C` in the terminal to stop the server.

## Tests

Run the automated test suite from the repository root with the virtual environment active:

```bash
pytest
```

## Deployment

The live product URL should be public and accessible to graders:

**Application URL:** [Add the deployed URL here](https://your-live-app-url.example)

This repository includes a Render deployment blueprint in `render.yaml`. A deployment needs a PostgreSQL database and the following environment variables configured by the host:

- `SECRET_KEY` — a secure, unique secret generated for the deployment
- `DATABASE_URL` — the PostgreSQL connection string
- `ADMIN_EMAIL` and `ADMIN_PASSWORD` — optional values used by the startup script to create or update the administrator account

Never commit production credentials, secret keys, or a populated `.env` file. After deploying, open the public URL and verify the main pages and core user flows before sharing it for assessment.

## Summative submission checklist

- [ ] Replace the live application URL placeholders above with the real deployed URL.
- [ ] Record a 5–10 minute video covering the system description, problem, why it matters, proposed solution, and a prototype demo.
- [ ] Add the video link to the Google Doc.
- [ ] Add this public GitHub repository link to the Google Doc: <https://github.com/Oluwatomi-Thompson/tera>
- [ ] Add the SRS link to the Google Doc: <https://github.com/Oluwatomi-Thompson/tera/blob/main/docs/srs/Oluwatomi_Thompson_Assignment2_10262026.pdf>
- [ ] Check that the Google Doc and video permissions allow the grader to open them.
- [ ] Submit the Google Doc link on Canvas by 25 November 2026.

Use the required Google Doc title format: `personNames_[Summative]_[MMDDYYYY]`.
