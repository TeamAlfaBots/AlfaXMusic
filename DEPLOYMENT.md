# AlfaXMusic Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Deployment](#local-deployment)
3. [VPS Deployment](#vps-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Heroku Deployment](#heroku-deployment)
6. [MongoDB Setup](#mongodb-setup)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying AlfaXMusic, ensure you have:

- Python 3.10 or higher
- MongoDB database (local or cloud)
- Telegram API credentials (API_ID, API_HASH)
- Bot Token from [@BotFather](https://t.me/BotFather)
- FFmpeg installed

---

## Local Deployment

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/AlfaXMusic.git
cd AlfaXMusic
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

### Step 5: Generate Session String (Optional)

```bash
python3 session_generator.py
```

### Step 6: Run the Bot

```bash
bash start.sh
```

Or directly:

```bash
python3 -m AlfaXmusic
```

---

## VPS Deployment

### Ubuntu/Debian

#### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Dependencies

```bash
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

#### 3. Install MongoDB

```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update and install
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### 4. Setup Bot

```bash
# Clone repository
git clone https://github.com/yourusername/AlfaXMusic.git
cd AlfaXMusic

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env
```

#### 5. Create Systemd Service

```bash
sudo nano /etc/systemd/system/alfaxmusic.service
```

Add:

```ini
[Unit]
Description=AlfaXMusic Telegram Bot
After=network.target mongod.service

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/AlfaXMusic
Environment=PATH=/home/yourusername/AlfaXMusic/venv/bin
ExecStart=/home/yourusername/AlfaXMusic/venv/bin/python -m AlfaXmusic
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 6. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable alfaxmusic
sudo systemctl start alfaxmusic
```

#### 7. Monitor Logs

```bash
sudo journalctl -u alfaxmusic -f
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/AlfaXMusic.git
cd AlfaXMusic

# Configure environment
cp .env.example .env
nano .env

# Start with Docker Compose
docker-compose up -d
```

### Using Docker

```bash
# Build image
docker build -t alfaxmusic .

# Run container
docker run -d \
  --name alfaxmusic \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  alfaxmusic
```

---

## Heroku Deployment

### Using Heroku CLI

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set MONGO_URI=your_mongo_uri
heroku config:set OWNER_ID=your_user_id

# Deploy
git push heroku main
```

### Using Heroku Button

Click the button below to deploy directly to Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

---

## MongoDB Setup

### Local MongoDB

```bash
# Install MongoDB (Ubuntu)
sudo apt install mongodb

# Start service
sudo systemctl start mongodb

# Connection string
MONGO_URI=mongodb://localhost:27017/AlfaXMusic
```

### MongoDB Atlas (Cloud)

1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Add your IP to whitelist
4. Create a database user
5. Get connection string

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/AlfaXMusic?retryWrites=true&w=majority
```

---

## Environment Variables

### Required

| Variable | Description | How to Get |
|----------|-------------|------------|
| `API_ID` | Telegram API ID | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Bot Token | [@BotFather](https://t.me/BotFather) |
| `MONGO_URI` | MongoDB URL | MongoDB Atlas or local |
| `OWNER_ID` | Your User ID | [@userinfobot](https://t.me/userinfobot) |

### Optional

| Variable | Description |
|----------|-------------|
| `SESSION_STRING` | Userbot session for better performance |
| `SPOTIFY_CLIENT_ID` | Spotify API credentials |
| `SPOTIFY_CLIENT_SECRET` | Spotify API credentials |
| `START_IMG_URL` | Image for /start command |
| `PING_IMG_URL` | Image for /ping command |

---

## Troubleshooting

### Bot Not Starting

1. Check logs: `sudo journalctl -u alfaxmusic -f`
2. Verify environment variables
3. Check MongoDB connection
4. Ensure FFmpeg is installed

### Voice Chat Issues

1. Make sure userbot session is configured
2. Check if bot has voice chat permissions
3. Verify PyTgCalls is properly installed

### MongoDB Connection Failed

1. Check MongoDB is running: `sudo systemctl status mongod`
2. Verify connection string
3. Check firewall settings

### Module Not Found

```bash
pip install -r requirements.txt --upgrade
```

---

## Support

- Telegram: [@YourSupportGroup](https://t.me/YourSupportGroup)
- Issues: [GitHub Issues](https://github.com/yourusername/AlfaXMusic/issues)

---

**Powered by Alfa Bots** © 2024
