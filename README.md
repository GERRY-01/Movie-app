# 🎬 MovieStream – Django Movie Streaming App

## 🚀 Features

- 🔍 Search for movies and TV shows
- 📃 View detailed descriptions and posters
- 📺 Watch movies directly from embedded sources
- 📚 Browse seasons and episodes for TV shows
- 🔥 Trending and Top Rated sections
- 💻 Responsive design with Tailwind CSS
- ☁️ Deployable on render

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, Tailwind CSS
- **API**: [TMDb API](https://developer.themoviedb.org/)
- **Streaming**: VidSrc
- **Deployment**: Render

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/GERRY-01/Movie-app
cd moviesite
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env file
In the root folder, create a .env file and add:

```bash
SECRET_KEY=your_django_secret_key
API_KEY=your_tmdb_api_key
```

### 5. Run the app

```bash
python manage.py runserver
```

### Thisis the link of the deployed app

https://movie-app-7yxu.onrender.com
