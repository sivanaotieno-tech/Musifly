# 🎵 Musifly

A modern music streaming application that integrates with Spotify's API. Built with TypeScript frontend and Python Flask backend.

## 🚀 Features

### Frontend (TypeScript)
- ✅ **Secure OAuth Authentication** - PKCE flow for secure authorization
- 🎨 **Modern UI** - Built with TypeScript and HTML/CSS
- 🔐 **Session Management** - Automatic token refresh and storage
- 📱 **Responsive Design** - Works on desktop and mobile devices

### Backend (Python/Flask)
- 🔐 **OAuth2 Authentication** - Secure Spotify API integration
- 🎵 **User Profile Data** - Access user's Spotify profile information
- 📊 **Top Tracks** - View user's top tracks (short, medium, long term)
- 💾 **Saved Tracks** - Browse liked songs
- 🔍 **Search Functionality** - Search for tracks, artists, and albums
- 💡 **Recommendations Engine** - Get personalized recommendations
- 🔄 **Token Management** - Automatic token refresh and validation

## 📁 Project Structure

```
SPOTIFY_CLONE/
├── frontend/                  # TypeScript/JavaScript frontend
│   ├── spotify.ts            # Main Spotify API client
│   ├── index.html            # HTML entry point
│   ├── index.css             # Styling
│   ├── vite-env.d.ts         # Vite type definitions
│   ├── tsconfig.json         # TypeScript configuration
│   └── package.json          # Frontend dependencies
│
├── backend/                   # Python Flask backend
│   ├── app.py               # Flask application & API routes
│   ├── spotify_auth.py      # Spotify OAuth manager
│   ├── requirements.txt     # Python dependencies
│   ├── setup.py            # Setup script
│   ├── .env.example        # Example environment variables
│   └── README.md           # Backend documentation
│
├── .env.example            # Environment variables template
├── .gitignore             # Git ignore patterns
└── README.md              # This file
```

## 🛠️ Prerequisites

### Frontend
- Node.js 16+ and npm/yarn
- Modern web browser

### Backend
- Python 3.8+
- Spotify Developer Account (free at https://developer.spotify.com)

## 🔧 Setup & Installation

### 1. Clone & Navigate

```bash
cd SPOTIFY_CLONE
```

### 2. Backend Setup

```bash
cd backend

# Create .env file
copy .env.example .env  # Windows
# or
cp .env.example .env    # Mac/Linux

# Edit .env with your Spotify credentials
# (Get from https://developer.spotify.com/dashboard)

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py
```

Backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on `http://localhost:5173` (or similar port)

## 🔑 Getting Spotify API Credentials

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in (create account if needed)
3. Click "Create an App"
4. Accept terms and create app
5. Copy **Client ID** and **Client Secret**
6. Click "Edit Settings"
7. Add Redirect URI: `http://localhost:5000/api/auth/callback`
8. Add these to your `.env` file:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:5000/api/auth/callback
```

## 🌐 API Endpoints

### Authentication
- `GET /api/auth/login` - Get authorization URL
- `GET /api/auth/callback` - Handle OAuth callback
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/token` - Get current access token

### User Data
- `GET /api/user/profile` - Current user's profile
- `GET /api/user/top-tracks` - User's top tracks
- `GET /api/user/saved-tracks` - User's liked songs

### Search & Discovery
- `GET /api/search` - Search for tracks/artists/albums
- `GET /api/recommendations` - Get recommendations

See [Backend README](./backend/README.md) for detailed API documentation.

## 🚀 Deployment

### For Production

1. **Environment Variables**
   - Change `FLASK_SECRET_KEY` to a strong random value
   - Update `SPOTIFY_REDIRECT_URI` to your production domain
   - Set `FLASK_DEBUG=False`

2. **Backend Deployment** (using Heroku, Render, etc.)
   ```bash
   # Example with Heroku
   heroku create your-app-name
   heroku config:set SPOTIFY_CLIENT_ID=...
   heroku config:set SPOTIFY_CLIENT_SECRET=...
   # ... set other env variables
   git push heroku main
   ```

3. **Frontend Deployment** (using Vercel, Netlify, etc.)
   - Update API base URL to production backend URL
   - `npm run build`
   - Deploy the `dist` folder

## 📝 Development Guide

### Adding New API Endpoints

1. **Backend** - Add route in `backend/app.py`:
   ```python
   @app.route('/api/new-endpoint', methods=['GET'])
   def new_endpoint():
       token_info = session.get('token_info')
       if not token_info:
           return jsonify({'error': 'Not authenticated'}), 401
       
       spotify = auth_manager.get_spotify_client(token_info)
       result = spotify.some_method()
       return jsonify(result), 200
   ```

2. **Frontend** - Call endpoint in TypeScript:
   ```typescript
   const response = await fetch('http://localhost:5000/api/new-endpoint', {
       headers: {
           'Authorization': `Bearer ${accessToken}`
       }
   });
   ```

## 🐛 Troubleshooting

### Backend Issues

**"Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET"**
- Create `.env` file from `.env.example`
- Add your Spotify credentials
- Restart backend

**"Connection refused" on port 5000**
- Make sure backend is running: `python app.py`
- Check if another app is using port 5000

**CORS errors**
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Make sure backend and frontend are on different ports

### Frontend Issues

**Can't connect to backend**
- Verify backend is running on http://localhost:5000
- Check browser console for CORS errors
- Make sure Spotify redirect URI matches

**Authentication not working**
- Verify Client ID and Secret in `.env`
- Check Spotify Developer Dashboard for correct redirect URI
- Clear browser cache and try again

## 🔒 Security Best Practices

- ❌ Never commit `.env` file to GitHub
- ❌ Never hardcode credentials
- ✅ Use environment variables
- ✅ Use HTTPS in production
- ✅ Regenerate credentials if exposed
- ✅ Keep dependencies updated

## 📚 Documentation

- [Backend Documentation](./backend/README.md)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Spotipy Library](https://spotipy.readthedocs.io)
- [Flask Framework](https://flask.palletsprojects.com)

## 📄 License

MIT License - feel free to use this project for learning or as a foundation for your own projects.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the backend/README.md
3. Check Spotify API documentation
4. Open an issue with detailed error information

## 🎉 Credits

- Built with [Spotify Web API](https://developer.spotify.com)
- Frontend: TypeScript
- Backend: Python + Flask + Spotipy
- Authentication: OAuth 2.0 with PKCE

---

**Made with ❤️ for music lovers**

Happy coding! 🎵
