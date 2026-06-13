# Elevate Demo Deployment

Recommended free demo setup:

- Backend: Render Web Service
- Frontend: Netlify or Vercel Static Site

## 1. Backend on Render

Create a new Render Web Service from this repository.

Use these settings if you configure it manually:

```text
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT
```

Add this environment variable in Render:

```text
GROQ_API_KEY=your_groq_api_key
```

After deployment, Render will give you a URL like:

```text
https://your-service-name.onrender.com
```

## 2. Frontend on Netlify or Vercel

The frontend currently points to the default Render service name from `render.yaml`:

```text
frontend/config.js
```

If Render gives you a different backend URL, update it here:

```js
window.ELEVATE_API_BASE_URL = "https://your-service-name.onrender.com";
```

For Netlify:

```text
Publish directory: frontend
Build command: none
```

For Vercel:

```text
Framework preset: Other
Output directory: frontend
Build command: empty / none
```

## Demo Notes

- The handwritten answer image upload may not work on Render unless Tesseract is installed.
- The normal Q&A, revision, quiz, analysis, practice answer text evaluation, and assistant backend voice answer route are wired for deployment.
- Render free services can sleep after inactivity, so the first request may be slow.
