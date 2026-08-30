# 🚀 Deployment Guide

## Option 1: Streamlit Community Cloud (Recommended)

### Step 1: Prepare GitHub Repository
```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: Customer Churn Prediction Platform"

# Create GitHub repository at github.com/new
git branch -M main
git remote add origin https://github.com/yourusername/customer_churn_prediction.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your GitHub repository
4. Choose **Branch**: `main`
5. Set **Main file path**: `app.py`
6. Click **"Deploy"**

**Deployment automatically starts!** 🎉

### Step 3: Share Your App
- Your app will be available at: `https://<username>-customer-churn-prediction.streamlit.app`
- Share the link with stakeholders

---

## Option 2: Docker Deployment

### Prerequisites
- Docker installed ([docker.com](https://docker.com))

### Deploy Locally with Docker

```bash
# Build image
docker build -t churn-prediction:latest .

# Run container
docker run -p 8501:8501 churn-prediction:latest

# Access at http://localhost:8501
```

### Deploy with Docker Compose
```bash
docker-compose up -d

# Stop
docker-compose down
```

### Push to Docker Hub
```bash
docker tag churn-prediction:latest yourusername/churn-prediction:latest
docker login
docker push yourusername/churn-prediction:latest
```

---

## Option 3: AWS Deployment

### Option 3a: AWS EC2 (Simple)

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t2.small (minimum)
   - Security group: Allow port 8501

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   git clone https://github.com/yourusername/customer_churn_prediction.git
   cd customer_churn_prediction
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run Streamlit**
   ```bash
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   ```

5. **Access**
   - `http://your-instance-ip:8501`

### Option 3b: AWS ECS (Production)

```bash
# Create ECR repository
aws ecr create-repository --repository-name churn-prediction

# Push image
docker tag churn-prediction:latest <account-id>.dkr.ecr.<region>.amazonaws.com/churn-prediction:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/churn-prediction:latest

# Deploy to ECS Fargate
# (Configure via AWS Console or CloudFormation)
```

---

## Option 4: Heroku Deployment

### Prepare Heroku Files

1. **Create Procfile**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   echo "[theme]
   primaryColor = \"#1f77b4\"
   backgroundColor = \"#ffffff\"
   secondaryBackgroundColor = \"#f0f2f6\"
   textColor = \"#31333f\"
   font = \"sans serif\"
   
   [client]
   showErrorDetails = true
   
   [server]
   port = \$PORT
   headless = true
   " > ~/.streamlit/config.toml
   ```

3. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

---

## Option 5: Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project/churn-prediction

# Deploy
gcloud run deploy churn-prediction \
  --image gcr.io/your-project/churn-prediction \
  --platform managed \
  --region us-central1 \
  --port 8501 \
  --memory 512Mi
```

---

## Option 6: DigitalOcean App Platform

1. Push code to GitHub
2. Login to [DigitalOcean](https://www.digitalocean.com/)
3. Click **"Create"** → **"Apps"**
4. Select your GitHub repository
5. Configure:
   - **Build command**: `pip install -r requirements.txt`
   - **Run command**: `streamlit run app.py`
   - **HTTP Port**: 8501
6. Click **"Deploy"**

---

## Production Checklist

- [ ] Environment variables configured
- [ ] Error handling tested
- [ ] Model files present and accessible
- [ ] Dependencies in requirements.txt
- [ ] Security: No API keys in code
- [ ] Performance: App loads <3 seconds
- [ ] Mobile responsive tested
- [ ] Analytics enabled (optional)
- [ ] Monitoring configured
- [ ] Backup strategy in place

---

## Performance Optimization

### Caching Strategies
```python
@st.cache_resource
def load_model():
    # Loaded once per session
    return model

@st.cache_data
def load_data():
    # Cached across reruns
    return data
```

### Streamlit Configuration
```toml
[client]
maxCacheMessageSize = 200

[logger]
level = "warning"
```

---

## Monitoring & Logs

### Streamlit Cloud
- View logs in **App settings** → **Advanced settings** → **Logs**

### Docker
```bash
# View logs
docker logs container-id

# Stream logs
docker logs -f container-id
```

### AWS CloudWatch
- Monitor EC2/ECS metrics
- Set up alarms for performance issues

---

## Troubleshooting Deployments

### Issue: Model Files Not Found
```
Solution: Ensure churn_model.pkl and model_columns.pkl are committed to git
```

### Issue: Port Already in Use
```bash
# Kill process using port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port 8502
```

### Issue: Memory Limit Exceeded
- Increase instance memory
- Optimize data loading with caching
- Use streaming for large datasets

### Issue: Slow App Performance
- Enable Streamlit caching
- Profile code with streamlit_profiler
- Use CDN for static assets

---

## Security Best Practices

1. **Use environment variables for secrets**
   ```python
   import os
   api_key = os.getenv("API_KEY")
   ```

2. **Enable HTTPS** (automatic on Streamlit Cloud)

3. **Set up access control** (if needed)
   ```python
   if not authenticate_user():
       st.stop()
   ```

4. **Regular security updates**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

5. **Monitor logs for suspicious activity**

---

## Scaling Considerations

### For Small Load (<100 users)
- Streamlit Cloud ✅
- Single EC2 instance ✅

### For Medium Load (100-1000 users)
- AWS ECS with load balancer
- DigitalOcean App Platform
- Kubernetes cluster

### For Large Load (1000+ users)
- Kubernetes with auto-scaling
- API layer (FastAPI)
- Separate prediction service
- Caching layer (Redis)

---

## Cost Estimates

| Platform | Estimated Monthly Cost |
|----------|----------------------|
| Streamlit Cloud | Free (public) / $5-50 |
| AWS EC2 (t2.small) | $7-15 |
| DigitalOcean | $5-12 |
| Heroku | $7+ |
| Google Cloud Run | Pay-per-use (~$5-20) |

---

## Support Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-cloud)
- [Docker Docs](https://docs.docker.com/)
- [AWS Documentation](https://aws.amazon.com/documentation/)

---

<div align="center">

**Choose the deployment option that best fits your needs!**

For most use cases, **Streamlit Community Cloud** is the easiest and fastest option.

</div>
