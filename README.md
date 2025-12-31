# FollowWise 🚀

**AI-Powered Sales Follow-Up Automation for Freelancers & Agencies**

FollowWise is a full-stack SaaS MVP designed to automate the tedious process of writing sales follow-up emails. It uses AI to generate context-aware, personalized email drafts in seconds, helping users close more deals with less effort.

![FollowWise Dashboard](docs/images/dashboard-preview.png)
*(Add a screenshot or GIF of your dashboard here)*

## 🌟 Key Features

* **🤖 AI Email Generation:** Instantly generate 3 distinct follow-up variations (Polite, Assertive, Friendly) using LLMs (NVIDIA/OpenAI compatible).
* **📊 Interactive Dashboard:** specific "Welcome" animations powered by **GSAP** and smooth page transitions with **Framer Motion**.
* **💼 Lead Management:** Full CRUD capabilities to track leads, status, and interaction history.
* **🔐 Secure Authentication:** JWT-based login/registration with industry-standard password hashing (Argon2/Bcrypt).
* **📧 Email Logging:** "Send" emails directly from the app (currently logs to database for MVP) and track history.
* **📱 Responsive Design:** Built with **Tailwind CSS** for a mobile-first, modern UI.

## 🛠️ Tech Stack

### **Frontend**
* **Framework:** React (Vite)
* **Styling:** Tailwind CSS
* **Animations:** GSAP (Intro sequences), Framer Motion (Page transitions & interactions)
* **Routing:** React Router v6
* **HTTP Client:** Axios with Interceptors
* **Notifications:** React Hot Toast

### **Backend**
* **Framework:** FastAPI (Python 3.10+)
* **Database:** SQLite (Production-ready for MVP, easily swappable for PostgreSQL)
* **ORM:** SQLAlchemy + Pydantic
* **Authentication:** OAuth2 with JWT Tokens
* **AI Layer:** Custom `AIProvider` Strategy Pattern (Hot-swappable providers)

---

## 🚀 Getting Started

### Prerequisites
* Node.js (v18+)
* Python (v3.8+)
* Git

### 1. Clone the Repository
```bash
git clone [https://github.com/nik-767/FOLLOW-WISE.git](https://github.com/nik-767/FOLLOW-WISE.git)
cd followwise
