# PocketSmart AI

PocketSmart AI is a FastAPI + Jinja2 web application based on the supplied project documentation. It provides:

- Home Interior budget planning
- Party budget planning
- Jewelry recommendations with optional outfit-image analysis
- Gemini-powered structured recommendations
- Safe mock product/vendor catalogs for local development
- User registration/login/logout
- JWT token endpoint
- Session information and session data endpoints
- Recommendation history
- Responsive HTML/CSS/JavaScript UI
- SQLite persistence with SQLAlchemy
- Automatic fallback recommendations when Gemini is unavailable

The supplied documentation describes Gemini 1.5 Flash Pro. Because Gemini model availability changes, this implementation makes the model configurable through `GEMINI_MODEL`; the default is a current configurable Flash model. If you specifically have access to a different Gemini model, change that one environment variable.

## 1. Requirements

- Python 3.11+
- VS Code
- A Gemini API key for AI mode
- Windows/macOS/Linux

No Node.js installation is required.

## 2. Create the environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can run the interpreter directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure environment variables

Copy `.env.example` to `.env`.

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///./pocketsmart.db
AI_ENABLED=true
```

If you do not have a Gemini key yet, set:

```text
AI_ENABLED=false
```

The app will still run using the built-in mock catalog/fallback engine.

## 4. Run

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## 5. Test

Run:

```bash
pytest -q
```

The tests cover health, registration/login, protected routes, planner validation, mock-mode recommendation generation, session data, and history.

## 6. Planner API examples

### Home

```bash
curl -X POST http://127.0.0.1:8000/generate-home \
  -H "Content-Type: application/json" \
  -d "{\"budget\":50000,\"rooms\":[{\"room_type\":\"Living Room\",\"items\":[{\"name\":\"Ceiling light\",\"quantity\":2},{\"name\":\"Coffee table\",\"quantity\":1}]}],\"style\":\"Modern\",\"city\":\"Bengaluru\"}"
```

### Party

```bash
curl -X POST http://127.0.0.1:8000/generate-party \
  -H "Content-Type: application/json" \
  -d "{\"budget\":40000,\"guest_count\":30,\"event_type\":\"Birthday\",\"venue_type\":\"Home\",\"city\":\"Bengaluru\",\"food_preference\":\"Vegetarian\",\"decoration_style\":\"Colorful\"}"
```

### Jewelry

Use the browser UI for multipart image upload, or POST text-only JSON to:

```text
POST /generate-jewelry
```

The multipart browser form also accepts an optional image.

## 7. Important implementation note

The project documentation describes Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO as sources. This implementation deliberately uses a local mock catalog instead of scraping or pretending to have live third-party inventory. Each recommendation contains a platform label and a generated search URL. This keeps the project runnable without undocumented credentials or brittle scraping.

For production, replace `app/services/catalog.py` with official partner/API integrations and add live availability/price verification before displaying prices as current.

## 8. Security notes

- Passwords are salted and hashed with PBKDF2-HMAC-SHA256.
- JWTs are signed using `SECRET_KEY`.
- Passwords are never returned by API responses.
- Uploaded jewelry images are validated by MIME type and size.
- Uploaded images are kept in memory and are not permanently stored.
- The demo uses SQLite; production deployments should use PostgreSQL or another managed database.
- Set a strong random `SECRET_KEY` in production.
