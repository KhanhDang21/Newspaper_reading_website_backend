# 📰 Newspaper Reading Website — Backend

Backend API for an online newspaper reading platform, built with **FastAPI** and featuring an automated news crawler that runs continuously in the background.

---

## 🚀 Features

- **User Authentication** — Register and login with JWT (python-jose + bcrypt)
- **Article Management** — Full CRUD for news articles with pagination
- **Auto News Crawling** — Automatically fetches articles from multiple news sources every 2 minutes as a background task
- **Tag System** — Tag articles and let users follow topics of interest
- **Comments** — Users can comment on individual articles
- **Reading History** — Tracks articles read by each user
- **Publishers** — Manage newspaper sources and publishers
- **Search** — Full-text search endpoint for articles

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.115 |
| Database | MongoDB (Motor async driver + Beanie ODM) |
| Cache | Redis 6 |
| Auth | JWT via python-jose, passwords hashed with bcrypt / passlib |
| Validation | Pydantic v2 |
| Pagination | fastapi-pagination |
| Runtime | Uvicorn (ASGI) |
| Containerization | Docker + Docker Compose |

---

## 📁 Project Structure

```
.
├── main.py               # App entry point — starts server & background crawler
├── adapter.py            # Saves crawled articles to the database
├── ai_crawl.py           # Auto news crawler logic
├── configs/              # Database config and environment setup
├── models/               # Beanie document models (MongoDB collections)
├── routers/              # API route handlers
│   ├── authentication_router.py
│   ├── user_info_router.py
│   ├── post_router.py
│   ├── newspaper_publisher_router.py
│   ├── tag_router.py
│   ├── comment_router.py
│   ├── search_router.py
│   ├── post_tag_router.py
│   ├── post_read_router.py
│   ├── user_info_tag_router.py
│   └── user_info_post_router.py
├── schemas/              # Pydantic request / response schemas
├── services/             # Business logic layer
├── requirements.txt
├── Dockerfile
└── compose.yaml
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- A running MongoDB instance (local or Atlas)
- A running Redis instance
- *(Or use Docker to skip the above requirements)*

### 1. Run Manually

```bash
# 1. Clone the repository
git clone https://github.com/KhanhDang21/Newspaper_reading_website_backend.git
cd Newspaper_reading_website_backend

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file (see Environment Variables below)

# 5. Start the server
uvicorn main:app --reload
```

Server runs at: [http://localhost:8000](http://localhost:8000)

Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Run with Docker Compose *(recommended)*

```bash
docker-compose up --build
```

This will spin up the backend, MongoDB, and Redis together.

---

## 🔑 Environment Variables

Create a `.env` file at the project root:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=newspaper_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 📡 API Endpoints

All routes are prefixed with `/api`.

| Group | Prefix | Description |
|---|---|---|
| Auth | `/api/auth` | Register, login, token refresh |
| Users | `/api/users` | User profile management |
| Posts | `/api/posts` | Articles — CRUD and pagination |
| Publishers | `/api/publishers` | News source / publisher management |
| Tags | `/api/tags` | Tag management |
| Comments | `/api/comments` | Article comments |
| Search | `/api/search` | Article search |
| Post-Tag | `/api/post-tags` | Link articles to tags |
| Read History | `/api/post-reads` | User reading history |
| User-Tag | `/api/user-tags` | User's followed tags |
| User-Post | `/api/user-posts` | User's saved articles |

Full interactive documentation is available at `/docs` once the server is running.

---

## 🤖 Auto-Crawl Mechanism

On startup, a background task launches an infinite loop:

1. Calls `AutoNewsCrawler.crawl_multiple_urls()` to fetch articles from configured news sources
2. Saves each article to MongoDB via `adapter.save_crawled_article()`
3. Sleeps for **120 seconds**, then repeats

If any error occurs, the crawler automatically retries after 10 seconds.

---

## 🐳 Docker

For more details on Docker usage, see [`README.Docker.md`](./README.Docker.md).

```bash
# Build the image
docker build -t newspaper-backend .

# Run with Compose (includes MongoDB + Redis)
docker-compose up --build
```

---

## 👤 Author

**KhanhDang21** — [GitHub](https://github.com/KhanhDang21)

---

## 📄 License

This project does not currently have a license. Please contact the author before using it for commercial purposes.
