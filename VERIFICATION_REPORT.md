**Summary**
- **Project**: FollowWise monorepo
- **Goal**: Verify implementation vs App Goal (FastAPI backend + React frontend MVP with AI dummy and Gmail stubs).

**Backend — What Meets Requirements**
- **App entry / routers**: `backend/app/main.py` registers `/api/auth`, `/api/leads`, `/api/users` and health route. See [backend/app/main.py](backend/app/main.py#L1-L80).
- **Auth endpoints**: `/api/auth/register`, `/api/auth/login`, `/api/auth/me` implemented in [backend/app/api/endpoints/auth.py](backend/app/api/endpoints/auth.py#L1-L120). Uses password hashing and JWT creation via `app/core/security.py`.
- **JWT & bcrypt**: JWT creation/verification in [backend/app/core/security.py](backend/app/core/security.py#L1-L200); password hashing via Passlib `bcrypt` scheme is used.
- **Database**: SQLite configured by default in [backend/app/db/base.py](backend/app/db/base.py#L1-L50).
- **Models & schemas**: SQLAlchemy models for `User`, `Lead`, `FollowUpSuggestion`, and `SentEmailLog` exist in `backend/app/models/*` and matching Pydantic schemas in `backend/app/schemas/*`.
- **AI layer (dummy)**: `backend/app/ai/providers.py` implements `AIProvider` and `DummyAIProvider` returning 3 variants; DI helper `get_ai_provider()` present.
- **Followup generation endpoint**: `POST /api/leads/{lead_id}/generate-followups` implemented in [backend/app/api/endpoints/leads.py](backend/app/api/endpoints/leads.py#L1-L160) and saves suggestions to DB.
- **Email logging**: Sending is stubbed by logging to DB via `SentEmailLog` in leads endpoints and `LeadService.log_sent_email`.

**Backend — Issues & Gaps**
- **Field name mismatches / minor inconsistencies**:
  - `User` model uses `hashed_password` but `auth.register` writes `hashed_password` — consistent. (OK)
  - `auth.py` returns `UserSchema` on register; `UserSchema` expects `id`, `created_at`, etc — registration populates them after commit (OK).
  - In `leads.py` send-email endpoint, code sets `status` on `SentEmailLog` even though model `SentEmailLog` has no `status` column. See [backend/app/models/sent_email_log.py](backend/app/models/sent_email_log.py#L1-L80) and [backend/app/api/endpoints/leads.py](backend/app/api/endpoints/leads.py#L200-L270). This will raise an error when creating sent email entries.
- **Gmail integration**:
  - No dedicated `integrations/gmail.py` file found. Email sending is currently stubbed by DB logging (acceptable for MVP), but the repo lacks the modular Gmail OAuth/send interface requested. Search results referenced Gmail in README and schemas but no implementation module.
- **AI provider usage**:
  - `DummyAIProvider` is implemented, but some provider functions return Pydantic models from a different schema module (`FollowUpSuggestionBase`) which is used directly — overall workable but requires small type checks if swapping real provider.

**Frontend — What Meets Requirements**
- **React app present** under `frontend/` with Vite setup and Tailwind classes used.
- **Auth UI & token handling**: Login/Register pages and `AuthContext` exist; JWT stored in `localStorage` and attached via Axios interceptor in `frontend/src/services/api.js`.
- **API wiring**: `frontend/src/services/api.js` calls match backend paths under `/api/*` (Axios base `VITE_API_URL` defaults to `http://localhost:8000/api`).

**Frontend — Issues & Gaps**
- **TypeScript requirement not met**: Frontend is implemented in JavaScript/JSX (files in `frontend/src` are `.jsx`), not TypeScript as specified in the App Goal.
- **Missing UI for AI follow-ups**: `LeadDetail.jsx` shows lead info but does not include the "Generate 3 follow-up emails" UI, tone select, or suggestion cards. `Leads.jsx` lacks an implemented "Add Lead" flow (button shows a toast placeholder).
- **Send/Copy UI**: No UI components currently call `generate-followups` or `send-email` endpoints; Sent Emails page is a placeholder.
- **Minor bugs**:
  - `AuthContext` imports `jwtDecode` incorrectly as named import (`import { jwtDecode } from 'jwt-decode'`), should use default import: `import jwtDecode from 'jwt-decode'`.
  - `api.auth.login` posts OAuth form to `/auth/login` but frontend `authApi.login` calls `api.post('/auth/login', params.toString(), ...)` — because Axios instance default baseURL includes `/api`, routing works but ensure form encoding is correct (current code sets headers to `application/x-www-form-urlencoded`).

**Missing Tests & Deployment Notes**
- Minimal or no unit tests found for core service functions (backend `tests/` exists but content not inspected in detail).
- Deployment readiness: Backend uses SQLite (good for free tiers). Frontend uses Vite (suitable for Vercel/Netlify) but is JS not TS.

**Immediate Fixes / Recommendations**
- Fix `SentEmailLog` inconsistency: either add a `status` column to the model or remove `status` assignment in [backend/app/api/endpoints/leads.py](backend/app/api/endpoints/leads.py#L200-L270).
- Add a Gmail integration module at `backend/app/integrations/gmail.py` that exposes stubbed functions `create_oauth_url()`, `exchange_code_for_tokens()`, and `send_email()` so the hook is present for later credentials. Keep implementation stubbed returning success for MVP.
- Implement frontend features:
  - Convert (or incrementally migrate) frontend to TypeScript if TypeScript is a hard requirement; otherwise note that it's currently JS and works for MVP.
  - Add UI to `LeadDetail.jsx` for generating follow-ups (tone selector + "Generate" button) that calls `leadsApi.generateFollowups` and displays `getFollowups` results with Copy/Send buttons.
  - Implement "Add Lead" modal/form to POST `/api/leads`.
- Fix `jwt-decode` import and ensure `AuthContext` decodes token payload correctly (or call `/api/auth/me` to fetch user info after login).

**How to run locally (quick)**
- Backend
  - Create a virtualenv and install requirements from `backend/requirements.txt`.
  - Run DB migrations (or let SQLAlchemy create tables) and start server:

```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Frontend

```bash
cd frontend
npm install
npm run dev
```

**Files inspected (examples)**
- [backend/app/main.py](backend/app/main.py)
- [backend/app/core/security.py](backend/app/core/security.py)
- [backend/app/models/lead.py](backend/app/models/lead.py)
- [backend/app/models/followup_suggestion.py](backend/app/models/followup_suggestion.py)
- [backend/app/models/sent_email_log.py](backend/app/models/sent_email_log.py)
- [backend/app/ai/providers.py](backend/app/ai/providers.py)
- [backend/app/api/endpoints/leads.py](backend/app/api/endpoints/leads.py)
- [frontend/src/services/api.js](frontend/src/services/api.js)
- [frontend/src/pages/LeadDetail.jsx](frontend/src/pages/LeadDetail.jsx)

**Next steps — pick one**
- I can create the missing `backend/app/integrations/gmail.py` stub now.
- I can implement the `LeadDetail` UI for generating followups and Send/Copy actions.
- I can patch the `SentEmailLog` issue (add `status` column or remove assignment).

Tell me which of the next steps you'd like me to do first and I'll proceed.
