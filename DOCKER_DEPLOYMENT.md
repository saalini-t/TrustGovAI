# TrustGov AI - Docker Deployment Guide

## 🚀 Quick Start with Docker

### Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (comes with Docker Desktop)

### Option 1: Run with Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/saalini-t/TrustGovAI.git
cd TrustGovAI

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Access the application:**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Run Backend Only

```bash
# Build the Docker image
docker build -t trustgov-ai .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e FAST_MODE=true \
  --name trustgov-backend \
  trustgov-ai

# View logs
docker logs -f trustgov-backend

# Stop the container
docker stop trustgov-backend
```

---

## 🌐 Deploy to Cloud Platforms

### Deploy to Railway.app (Free Tier Available)

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select the TrustGovAI repository
4. Railway will auto-detect the Dockerfile
5. Set environment variables:
   - `FAST_MODE=true`
   - `PORT=8000`
6. Click "Deploy"
7. Railway will provide a public URL

### Deploy to Render (Free Tier Available)

1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configuration:
   - **Name:** trustgov-ai
   - **Environment:** Docker
   - **Region:** Choose closest to users
   - **Instance Type:** Free (or paid for better performance)
5. Environment Variables:
   ```
   FAST_MODE=true
   PORT=8000
   ```
6. Click "Create Web Service"

### Deploy to Google Cloud Run

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/trustgov-ai

# Deploy to Cloud Run
gcloud run deploy trustgov-ai \
  --image gcr.io/YOUR_PROJECT_ID/trustgov-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FAST_MODE=true
```

### Deploy to AWS (Elastic Beanstalk)

1. Install AWS CLI and EB CLI
2. Initialize Elastic Beanstalk:
   ```bash
   eb init -p docker trustgov-ai
   ```
3. Create environment:
   ```bash
   eb create trustgov-production
   ```
4. Set environment variables:
   ```bash
   eb setenv FAST_MODE=true
   ```
5. Deploy:
   ```bash
   eb deploy
   ```

### Deploy to DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App" → "GitHub"
3. Select TrustGovAI repository
4. Configure:
   - **Type:** Web Service
   - **Environment:** Docker
   - **HTTP Port:** 8000
5. Environment Variables:
   ```
   FAST_MODE=true
   ```
6. Click "Create Resources"

---

## 🔧 Environment Variables

| Variable           | Default | Description                           |
| ------------------ | ------- | ------------------------------------- |
| `FAST_MODE`        | `true`  | Use fast retrieval mode (recommended) |
| `PORT`             | `8000`  | API server port                       |
| `PYTHONUNBUFFERED` | `1`     | Enable real-time logging              |

---

## 📦 Docker Commands Cheat Sheet

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Remove all data and rebuild
docker-compose down -v
docker-compose up -d --build

# Execute command in running container
docker-compose exec backend python -c "print('Hello')"

# Check container status
docker-compose ps

# View resource usage
docker stats
```

---

## 🐛 Troubleshooting

### Issue: Port already in use

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different ports
docker-compose up -d -p 9000:8000
```

### Issue: Container keeps restarting

```bash
# Check logs
docker-compose logs backend

# Check if models are loading
docker-compose exec backend ls -la /app
```

### Issue: Out of memory

- Use a machine with at least 2GB RAM
- Or deploy to a paid tier with more resources

### Issue: Slow response times

- First request is slow (model loading)
- Set `FAST_MODE=true` for faster responses
- Use a paid tier with more CPU/RAM

---

## 📊 Performance Optimization

### For Production Deployment:

1. **Use a reverse proxy (Nginx/Caddy)** for HTTPS
2. **Enable CDN** for frontend assets
3. **Use a larger instance type** (at least 2GB RAM)
4. **Set up monitoring** (health checks, logs)
5. **Configure auto-scaling** if available

---

## 🔒 Security Considerations

1. **Update CORS settings** in `app/main.py`:

   ```python
   allow_origins=["https://your-domain.com"]
   ```

2. **Add rate limiting** for API endpoints

3. **Use HTTPS** in production (most platforms provide this automatically)

4. **Set up authentication** if needed

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Support

For issues or questions:

- Open an issue on GitHub
- Check deployment platform documentation

---

**Built with ❤️ for TrustGov AI Hackathon**

