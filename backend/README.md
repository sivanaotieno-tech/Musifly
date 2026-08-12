# Musifly Backend

A Flask-based backend API for Musifly. This backend handles authentication, user data fetching, and search functionality using the Spotify Web API.

## Features

- 🔐 **OAuth2 Authentication** - Secure Spotify login using PKCE flow
- 🎵 **User Profile** - Get current user's profile information
- 📊 **Top Tracks** - Retrieve user's top tracks (short, medium, long term)
- 💾 **Saved Tracks** - Access user's liked songs
- 🔍 **Search** - Search for tracks, artists, and albums
- 💡 **Recommendations** - Get personalized track recommendations
- 🔄 **Token Management** - Automatic token refresh and validation

## Prerequisites

- Python 3.8 or higher
- Spotify Developer Account (free at https://developer.spotify.com)
- Virtual environment (recommended)

## Setup

### 1. Get Spotify API Credentials

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (create one if needed)
3. Create a new app
4. Accept the terms and create the app
5. Copy your **Client ID** and **Client Secret**
6. Add a redirect URI: `http://localhost:5000/api/auth/callback`

### 2. Set Up Environment

```bash
# Navigate to backend directory
cd backend

# Run setup script (Windows/Mac/Linux)
python setup.py

# Or manually create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Configure Credentials

```bash
# Copy example env file
cp .env.example .env  # On Windows: copy .env.example .env

# Edit .env and add your credentials
# SPOTIFY_CLIENT_ID=your_id_here
# SPOTIFY_CLIENT_SECRET=your_secret_here
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Backend

```bash
# Make sure virtual environment is activated
python app.py
```

The backend will start on `http://localhost:5000`

## API Endpoints

### Authentication

#### `GET /api/auth/login`
Initiate Spotify OAuth login flow
```json
Response: {"auth_url": "https://accounts.spotify.com/authorize?..."}
```

#### `GET /api/auth/callback`
Handle Spotify OAuth callback (Spotify redirects here)
```json
Response: {"success": true, "access_token": "..."}
```

#### `POST /api/auth/logout`
Logout current user
```json
Response: {"success": true, "message": "Logged out successfully"}
```

### User Data

#### `GET /api/user/profile`
Get current user's profile
```json
Response: {
  "display_name": "User Name",
  "email": "user@example.com",
  "external_urls": {...},
  "followers": {...},
  "href": "https://api.spotify.com/v1/users/...",
  "id": "user_id",
  "images": [...],
  "type": "user",
  "uri": "spotify:user:..."
}
```

#### `GET /api/user/top-tracks`
Get user's top tracks
```
Query Parameters:
  - limit: 1-50 (default: 20)
  - time_range: short_term, medium_term, long_term (default: medium_term)

Example: /api/user/top-tracks?limit=10&time_range=short_term
```

#### `GET /api/user/saved-tracks`
Get user's saved tracks (liked songs)
```
Query Parameters:
  - limit: 1-50 (default: 20)
  - offset: pagination offset (default: 0)

Example: /api/user/saved-tracks?limit=50&offset=0
```

### Search & Recommendations

#### `GET /api/search`
Search for tracks, artists, or albums
```
Query Parameters:
  - q: search query (required)
  - type: track, artist, album, playlist (default: track)
  - limit: 1-50 (default: 10)

Example: /api/search?q=Taylor+Swift&type=artist&limit=5
```

#### `GET /api/recommendations`
Get recommendations based on seeds
```
Query Parameters:
  - seed_tracks: comma-separated track IDs
  - seed_artists: comma-separated artist IDs
  - seed_genres: comma-separated genres
  - limit: 1-100 (default: 20)

Example: /api/recommendations?seed_artists=artist_id1,artist_id2&limit=10
```

### Health Check

#### `GET /api/health`
Check if backend is running
```json
Response: {"status": "Backend is running"}
```

## Environment Variables

```env
# Required - Get from Spotify Developer Dashboard
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret

# Optional - Change based on your deployment
SPOTIFY_REDIRECT_URI=http://localhost:5000/api/auth/callback
FLASK_SECRET_KEY=your-secret-key
FLASK_DEBUG=False

# Optional - Custom scopes (default includes common scopes)
SPOTIFY_SCOPES=user-read-private,user-read-email,user-library-read
```

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── spotify_auth.py        # Spotify OAuth authentication manager
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Troubleshooting

### "Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET"
- Make sure you created a .env file from .env.example
- Verify you added your credentials from the Spotify Developer Dashboard
- Make sure the .env file is in the backend directory

### "Connection refused on port 5000"
- Make sure no other application is using port 5000
- Check if Flask is actually running: look for "Running on http://localhost:5000"

### "Unauthorized" error when accessing endpoints
- Make sure you're logged in first by calling `/api/auth/login`
- Token may have expired - try logging out and back in

### CORS errors from frontend
- Make sure Flask-CORS is installed: `pip install flask-cors`
- The backend should be running on a different port than the frontend

## Development

### Running in Debug Mode

```bash
# Edit .env and set:
FLASK_DEBUG=True

# Run with debug mode enabled
python app.py
```

### Adding New Endpoints

1. Add a new route in `app.py`
2. Get token from session and validate
3. Use `auth_manager.get_spotify_client(token_info)` to interact with Spotify API
4. Return JSON response

Example:
```python
@app.route('/api/new-endpoint', methods=['GET'])
def new_endpoint():
    try:
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        spotify = auth_manager.get_spotify_client(token_info)
        # Use spotify client to fetch data
        result = spotify.some_method()
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

## Security Notes

- 🔒 Never commit `.env` file to version control
- 🔐 Change `FLASK_SECRET_KEY` in production
- 🛡️ Use HTTPS in production
- 📝 Regenerate `SPOTIFY_CLIENT_SECRET` if accidentally exposed

## License

This project is open source and available under the MIT License.

## Support

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [Spotipy Documentation](https://spotipy.readthedocs.io)
- [Flask Documentation](https://flask.palletsprojects.com)
