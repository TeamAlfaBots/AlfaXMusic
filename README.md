# AlfaXMusic - Telegram Music Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Powered%20by-Alfa%20Bots-orange.svg" alt="Powered by Alfa Bots">
</p>

A powerful, scalable, and feature-rich Telegram Music Bot built with Python, Pyrogram, and PyTgCalls.

## Features

- 🎵 **Music Streaming**: Play music from YouTube, Spotify, and Telegram
- 📋 **Queue Management**: Advanced queue system with add/remove/clear
- 🔁 **Playback Controls**: Loop, shuffle, pause, resume, skip
- 📂 **Playlist Support**: Predefined YAML playlists
- 👥 **Admin Controls**: Authorization system for group management
- 👑 **Sudo System**: Owner and sudo user management
- 📢 **Broadcast**: Send messages to all users and groups
- 🌍 **Multi-language**: Support for English, Hindi, and Bhojpuri
- 📊 **Statistics**: Track bot usage and performance
- 🐳 **Docker Ready**: Easy deployment with Docker

## Requirements

- Python 3.10+
- MongoDB
- FFmpeg
- Telegram API credentials

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AlfaXMusic.git
cd AlfaXMusic
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
nano .env
```

Required variables:
- `API_ID` - Get from [my.telegram.org](https://my.telegram.org)
- `API_HASH` - Get from [my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
- `MONGO_URI` - MongoDB connection string
- `OWNER_ID` - Your Telegram user ID

### 4. Generate Session String (Optional but Recommended)

```bash
python3 session_generator.py
```

Add the generated session string to your `.env` file.

### 5. Run the Bot

```bash
bash start.sh
```

Or directly:

```bash
python3 -m AlfaXmusic
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Using Docker

```bash
docker build -t alfaxmusic .
docker run -d --env-file .env alfaxmusic
```

## VPS Deployment

### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

### 3. Install MongoDB

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 4. Setup Bot

```bash
git clone https://github.com/yourusername/AlfaXMusic.git
cd AlfaXMusic
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
nano .env
```

### 5. Create Systemd Service

```bash
sudo nano /etc/systemd/system/alfaxmusic.service
```

Add the following:

```ini
[Unit]
Description=AlfaXMusic Telegram Bot
After=network.target mongod.service

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/AlfaXMusic
Environment=PATH=/path/to/AlfaXMusic/venv/bin
ExecStart=/path/to/AlfaXMusic/venv/bin/python -m AlfaXmusic
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable alfaxmusic
sudo systemctl start alfaxmusic
```

### 7. Monitor Logs

```bash
sudo journalctl -u alfaxmusic -f
```

## Heroku Deployment

### Using Heroku CLI

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set OWNER_ID=your_user_id

# Deploy
git push heroku main
```

### Using Heroku Button

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Commands

### Basic Commands
- `/start` - Start the bot
- `/help` - Show help menu
- `/ping` - Check bot latency

### Music Commands
- `/play <song>` - Play a song
- `/song <song>` - Download a song

### Queue Commands
- `/queue` - Show current queue
- `/skip` - Skip current song
- `/stop` - Stop playback
- `/pause` - Pause playback
- `/resume` - Resume playback

### Playback Controls
- `/loop` - Toggle loop mode
- `/shuffle` - Toggle shuffle mode
- `/volume <1-200>` - Set volume

### Admin Commands
- `/auth` - Authorize user
- `/unauth` - Unauthorize user
- `/authusers` - List authorized users

### Owner Commands
- `/broadcast` - Broadcast message
- `/stats` - Show statistics
- `/sudo` - Add sudo user
- `/rmsudo` - Remove sudo user
- `/sudolist` - List sudo users

### Playlist Commands
- `/play 90sHits` - Play 90s hits
- `/play Arijit Singh Sad` - Play sad songs
- `/play Arijit Singh Love` - Play love songs
- `/play Punjabi Hits` - Play Punjabi hits
- `/play Bhojpuri Hits` - Play Bhojpuri hits
- `/play Sad` - Play sad songs
- `/play Romantic` - Play romantic songs
- `/play Dance` - Play dance songs

## Project Structure

```
AlfaDemoBot/
├── AlfaXmusic/
│   ├── assets/           # Fonts and playlist files
│   ├── core/             # Core modules (bot, mongo, call, userbot)
│   ├── platform/         # Music platforms (YouTube, Spotify)
│   ├── plugins/          # Bot commands
│   │   ├── admin/        # Admin commands
│   │   ├── bot/          # Basic bot commands
│   │   ├── misc/         # Miscellaneous (broadcast)
│   │   ├── play/         # Music playback commands
│   │   ├── sudo/         # Sudo management
│   │   └── tools/        # Utility commands
│   ├── string/           # Language files
│   ├── utils/            # Utilities (decorators, thumbnails)
│   ├── __init__.py
│   ├── logging.py
│   ├── main.py           # Entry point
│   └── misc.py
├── config.py             # Configuration
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── start.sh              # Start script
└── README.md             # This file
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_ID` | Yes | Telegram API ID |
| `API_HASH` | Yes | Telegram API Hash |
| `BOT_TOKEN` | Yes | Bot token from @BotFather |
| `MONGO_URI` | Yes | MongoDB connection string |
| `OWNER_ID` | Yes | Owner's Telegram user ID |
| `SESSION_STRING` | No | Userbot session string |
| `SPOTIFY_CLIENT_ID` | No | Spotify API client ID |
| `SPOTIFY_CLIENT_SECRET` | No | Spotify API client secret |
| `START_IMG_URL` | No | Start command image |
| `PING_IMG_URL` | No | Ping command image |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- **Powered by Alfa Bots**
- Built with [Pyrogram](https://github.com/pyrogram/pyrogram)
- Voice calls by [PyTgCalls](https://github.com/pytgcalls/pytgcalls)

## Support

- Telegram: [@YourSupportGroup](https://t.me/YourSupportGroup)
- Updates: [@YourUpdatesChannel](https://t.me/YourUpdatesChannel)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<p align="center">
  <b>Powered by Alfa Bots</b><br>
  © 2024 Alfa Bots. All Rights Reserved.
</p>
