# AlfaXMusic - Project Summary

## Overview

**AlfaXMusic** is a production-grade Telegram Music Bot built with Python 3.10, featuring async architecture, MongoDB integration, multi-language support, and voice chat streaming capabilities.

---

## Project Structure

```
AlfaDemoBot/
├── AlfaXmusic/                 # Main bot package
│   ├── assets/                 # Fonts, playlists, thumbnails
│   │   ├── 90sHits.yml         # 90s hits playlist
│   │   ├── arijitsingh.yml     # Arijit Singh sad songs
│   │   ├── arijitsinghLove.yml # Arijit Singh love songs
│   │   ├── PunjabiHits.yml     # Punjabi hits playlist
│   │   ├── bhojpurihits.yml    # Bhojpuri hits playlist
│   │   ├── sad.yml             # Sad songs playlist
│   │   ├── romatic.yml         # Romantic songs playlist
│   │   ├── dance.yml           # Dance songs playlist
│   │   ├── font.ttf            # Regular font
│   │   ├── font2.ttf           # Bold font
│   │   ├── default_thumb.jpg   # Default thumbnail
│   │   └── silence.mp3         # Silence audio for calls
│   ├── core/                   # Core modules
│   │   ├── bot.py              # Pyrogram bot client
│   │   ├── call.py             # PyTgCalls voice handler
│   │   ├── mongo.py            # MongoDB database handler
│   │   └── userbot.py          # Userbot client
│   ├── platform/               # Music platform handlers
│   │   ├── youtube.py          # YouTube integration
│   │   ├── spotify.py          # Spotify integration
│   │   └── telegram.py         # Telegram audio handler
│   ├── plugins/                # Bot commands
│   │   ├── admin/              # Admin commands
│   │   │   └── auth.py         # Authorization system
│   │   ├── bot/                # Basic bot commands
│   │   │   ├── start.py        # Start command
│   │   │   └── help.py         # Help command
│   │   ├── misc/               # Miscellaneous
│   │   │   └── broadcast.py    # Broadcast system
│   │   ├── play/               # Music commands
│   │   │   ├── play.py         # Play command
│   │   │   └── queue.py        # Queue management
│   │   ├── sudo/               # Sudo management
│   │   │   └── sudo.py         # Sudo commands
│   │   └── tools/              # Utility commands
│   │       ├── ping.py         # Ping command
│   │       └── stats.py        # Statistics
│   ├── string/                 # Language system
│   │   ├── __init__.py         # Language loader
│   │   └── langs/
│   │       ├── En.yml          # English
│   │       ├── Hi.yml          # Hindi
│   │       └── Bh.yml          # Bhojpuri
│   ├── utils/                  # Utilities
│   │   ├── decorators.py       # Command decorators
│   │   ├── logger.py           # Logging utility
│   │   └── thumbnails.py       # Thumbnail generator
│   ├── __init__.py             # Package init
│   ├── logging.py              # Logging setup
│   ├── main.py                 # Entry point
│   └── misc.py                 # Miscellaneous helpers
├── config.py                   # Configuration
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose
├── start.sh                    # Start script
├── session_generator.py        # Session generator
├── app.json                    # Heroku config
├── heroku.yml                  # Heroku Docker
├── Procfile                    # Heroku Procfile
├── runtime.txt                 # Python runtime
├── .env.example                # Environment template
├── .gitignore                  # Git ignore
├── README.md                   # Main documentation
├── DEPLOYMENT.md               # Deployment guide
├── LICENSE                     # MIT License
└── PROJECT_SUMMARY.md          # This file
```

---

## Features

### Core Features
- ✅ Async architecture with Python 3.10+
- ✅ MongoDB database integration
- ✅ Multi-language support (English, Hindi, Bhojpuri)
- ✅ YAML-based playlist system
- ✅ Voice chat streaming with PyTgCalls
- ✅ Queue management system
- ✅ Admin and sudo user controls

### Music Platforms
- ✅ YouTube (search, URLs, playlists)
- ✅ Spotify (search, URLs, playlists)
- ✅ Telegram audio files

### Commands

#### Basic
- `/start` - Start the bot
- `/help` - Show help menu
- `/ping` - Check latency

#### Music
- `/play <song>` - Play music
- `/song <song>` - Download song

#### Queue
- `/queue` - Show queue
- `/skip` - Skip song
- `/stop` - Stop playback
- `/pause` - Pause playback
- `/resume` - Resume playback

#### Controls
- `/loop` - Toggle loop
- `/shuffle` - Toggle shuffle
- `/volume <1-200>` - Set volume

#### Admin
- `/auth` - Authorize user
- `/unauth` - Unauthorize user
- `/authusers` - List authorized users

#### Owner
- `/broadcast` - Broadcast message
- `/stats` - Show statistics
- `/sudo` - Add sudo user
- `/rmsudo` - Remove sudo user
- `/sudolist` - List sudo users

#### Playlists
- `/play 90sHits`
- `/play Arijit Singh Sad`
- `/play Arijit Singh Love`
- `/play Punjabi Hits`
- `/play Bhojpuri Hits`
- `/play Sad`
- `/play Romantic`
- `/play Dance`

---

## Database Schema

### Collections

#### users
```javascript
{
  user_id: Number,
  username: String,
  first_name: String,
  joined_at: Date,
  last_seen: Date
}
```

#### chats
```javascript
{
  chat_id: Number,
  title: String,
  type: String,
  added_at: Date,
  last_active: Date
}
```

#### playlists
```javascript
{
  chat_id: Number,
  song: Object,
  played_at: Date
}
```

#### stats
```javascript
{
  type: String,
  count: Number,
  updated_at: Date
}
```

#### sudo_users
```javascript
{
  user_id: Number,
  added_at: Date
}
```

#### settings
```javascript
{
  chat_id: Number,
  language: String,
  volume: Number,
  loop: Boolean,
  shuffle: Boolean,
  auto_play: Boolean
}
```

#### queue
```javascript
{
  chat_id: Number,
  queue: Array,
  updated_at: Date
}
```

---

## Environment Variables

### Required
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `BOT_TOKEN` - Bot token
- `MONGO_URI` - MongoDB connection string
- `OWNER_ID` - Owner user ID

### Optional
- `SESSION_STRING` - Userbot session
- `SPOTIFY_CLIENT_ID` - Spotify client ID
- `SPOTIFY_CLIENT_SECRET` - Spotify client secret
- `START_IMG_URL` - Start image URL
- `PING_IMG_URL` - Ping image URL
- `SUPPORT_URL` - Support group URL
- `UPDATES_URL` - Updates channel URL
- `REPO_URL` - Repository URL
- `DEV_URL` - Developer URL
- `PRIVACY_URL` - Privacy policy URL
- `ADD_GROUP_URL` - Add to group URL
- `QUESTIONS_URL` - FAQ URL

---

## Deployment Options

1. **Local** - Direct Python execution
2. **VPS** - Systemd service
3. **Docker** - Containerized deployment
4. **Heroku** - Cloud platform

---

## Dependencies

### Core
- pyrogram - Telegram MTProto client
- pytgcalls - Voice chat handler
- motor - Async MongoDB driver

### Platforms
- yt-dlp - YouTube downloader
- youtube-search-python - YouTube search
- spotipy - Spotify API

### Utilities
- pillow - Image processing
- pyyaml - YAML parsing
- aiohttp - Async HTTP

---

## Credits

**Powered by Alfa Bots**

© 2024 Alfa Bots. All Rights Reserved.

---

## License

MIT License - See LICENSE file for details.
