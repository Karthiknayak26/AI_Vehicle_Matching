# 🚀 Day 6: The "Stress-Free" Deployment Guide
## "How to put your AI System on the Internet"

**Role:** Senior DevOps Engineer  
**Goal:** Deploy your system safely for a demo without breaking anything.

---

## 1. The Strategy (Simple & Reliable)

We are splitting the deployment into two parts:
1.  **Backend (The Brain):** We will put FastAPI + Models on **Render.com**.
    - *Why:* It has great Python support and a free tier.
2.  **Frontend (The Face):** We will put React on **Vercel**.
    - *Why:* It's the standard for React apps, very fast, and zero config.

**The Golden Rule:** Deploy the Backend *first*. The Frontend needs the Backend's URL to work.

---

## 2. Backend Deployment (Render)

### ✅ Pre-Deployment Checklist
Before you leave your local machine:
1.  **Check `requirements.txt`:** It must have `fastapi` and `uvicorn`. (Checked: Yours is good!)
2.  **Check Models:** Ensure your `.pkl` files in `models/saved/` are pushed to GitHub.
    - *Why:* Render downloads your code from GitHub. If models aren't there, it crashes.
3.  **No Training:** We only *load* models. We do NOT run `train_eta_models.py` in production.

### 🛠️ Step-by-Step on Render
1.  Log in to [dashboard.render.com](https://dashboard.render.com/) with GitHub.
2.  Click **New +** -> **Web Service**.
3.  Connect your repository (`AI_Vehicle_Matching`).
4.  **Configuration:**
    - **Name:** `ride-match-api` (or similar)
    - **Region:** Singapore or nearest to you.
    - **Branch:** `main`
    - **Runtime:** `Python 3`
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5.  **Free Instance Type:** Select "Free".
6.  Click **Create Web Service**.

### ⏳ The Waiting Game (Cold Start)
- Render will install dependencies and start your app.
- Watch the logs. When you see `Application startup complete`, it's alive!
- **Copy your URL:** It will look like `https://ride-match-api.onrender.com`.

### ⚠️ Common Backend Issues
- **"Model not found":** You forgot to commit the `.pkl` files.
- **"Memory Error":** Your models are too big for the free tier (unlikely here, yours are optimized).
- **"Cold Start":** On the free plan, the server "sleeps" after 15 mins. The first request might take 50 seconds. *This is normal for a demo.*

---

## 3. Frontend Deployment (Vercel)

Now that we have a Backend URL, let's tell the Frontend where to talk.

### 🔌 Pre-Deployment: Dynamic API URL
Currently, your `api.js` points to `localhost:8000`. We need to change that.

**Recommended Change (Professional Way):**
Update `frontend/src/utils/api.js` to look for an Environment Variable:
```javascript
// Smart URL selection
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```
*(You will need to make this small code change before deploying).*

### 🛠️ Step-by-Step on Vercel
1.  Log in to [vercel.com](https://vercel.com/) with GitHub.
2.  Click **Add New...** -> **Project**.
3.  Import your repository.
4.  **Configure Project:**
    - **Framework Preset:** Vite (it usually auto-detects this).
    - **Root Directory:** Click "Edit" and select `frontend`. (CRITICAL STEP!)
5.  **Environment Variables:**
    - Click "Environment Variables".
    - **Name:** `VITE_API_BASE_URL`
    - **Value:** `https://ride-match-api.onrender.com` (Your Render URL from Section 2).
    - Click **Add**.
6.  Click **Deploy**.

---

## 4. Verification (Does it work?)

After Vercel finishes:

1.  **Open Deployed Frontend:** Click the domain Vercel gives you (e.g., `ai-vehicle-matching.vercel.app`).
2.  **Check Console:** Open Developer Tools (F12) -> Console. Make sure there are no red "Network Error" messages.
3.  **Test the Flow:**
    - Can you see the map?
    - When you click "Plan Ride", does it show the "Processing" animation?
    - Do vehicle cards appear?
    - **Success:** If cards appear, your Frontend successfully talked to your Backend!

---

## 5. Interview Explanation (The "Senior" Talk)

**Q: "How is this deployed?"**
> **A:** *"I used a decoupled architecture. The backend contains the ML models and runs on Render as a microservice. The frontend interacts with it via REST API and is hosted on Vercel for performance."*

**Q: "Why didn't you train the model in production?"**
> **A:** *"Training is resource-heavy and unstable. In production, we assume 'Inference Only' using pre-trained artifacts. This keeps the API fast and reliable."*

**Q: "What if traffic spikes?"**
> **A:** *"Currently, it's a single instance. In a real startup, I would use a load Balancer and auto-scale the backend instances based on CPU usage."*

---

## 📋 Final Checklist
- [ ] Backend is live (Status 200 on `/health`).
- [ ] Frontend environment variable is set.
- [ ] Frontend can fetch quotes from deployed backend.
- [ ] README updated with live links.

**Deployment Complete.** 🚀
