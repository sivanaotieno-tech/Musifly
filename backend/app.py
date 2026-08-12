"""
Spotify Clone Backend - Flask Application
Handles authentication and API endpoints for Spotify data
"""
import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from dotenv import load_dotenv
from spotify_auth import SpotifyAuthManager

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Initialize Spotify Auth Manager
auth_manager = SpotifyAuthManager()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Backend is running'}), 200


@app.route('/api/auth/login', methods=['GET'])
def login():
    """
    Initiate Spotify OAuth login flow
    Returns authorization URL
    """
    try:
        auth_url = auth_manager.get_auth_url()
        return jsonify({'auth_url': auth_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/auth/callback', methods=['GET'])
def callback():
    """
    Handle OAuth callback from Spotify
    Exchange authorization code for access token
    """
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not code:
            return jsonify({'error': 'No authorization code received'}), 400
        
        # Exchange code for tokens
        token_info = auth_manager.get_token(code, state)
        
        # Store token in session
        session['token_info'] = token_info
        
        return jsonify({
            'success': True,
            'message': 'Successfully authenticated',
            'access_token': token_info.get('access_token')
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/auth/token', methods=['GET'])
def get_token():
    """
    Get current access token
    """
    try:
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Refresh token if needed
        token_info = auth_manager.refresh_token_if_needed(token_info)
        session['token_info'] = token_info
        
        return jsonify({'access_token': token_info.get('access_token')}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """
    Logout user by clearing session
    """
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """
    Get current user's profile information
    """
    try:
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        spotify = auth_manager.get_spotify_client(token_info)
        user_profile = spotify.current_user()
        
        return jsonify(user_profile), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/user/top-tracks', methods=['GET'])
def get_top_tracks():
    """
    Get current user's top tracks
    Query parameters:
    - limit: number of tracks (default: 20, max: 50)
    - time_range: short_term, medium_term, long_term (default: medium_term)
    """
    try:
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        limit = request.args.get('limit', 20, type=int)
        time_range = request.args.get('time_range', 'medium_term')
        
        # Validate parameters
        limit = max(1, min(50, limit))  # Clamp between 1-50
        if time_range not in ['short_term', 'medium_term', 'long_term']:
            time_range = 'medium_term'
        
        spotify = auth_manager.get_spotify_client(token_info)
        results = spotify.current_user_top_tracks(limit=limit, time_range=time_range)
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/user/saved-tracks', methods=['GET'])
def get_saved_tracks():
    """
    Get current user's saved tracks (liked songs)
    Query parameters:
    - limit: number of tracks (default: 20, max: 50)
    - offset: pagination offset (default: 0)
    """
    try:
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        limit = max(1, min(50, limit))
        offset = max(0, offset)
        
        spotify = auth_manager.get_spotify_client(token_info)
        results = spotify.current_user_saved_tracks(limit=limit, offset=offset)
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/search', methods=['GET'])
def search():
    """
    Search for tracks, artists, albums
    Query parameters:
    - q: search query (required)
    - type: track, artist, album (default: track)
    - limit: results limit (default: 10, max: 50)
    """
    try:
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        q = request.args.get('q')
        search_type = request.args.get('type', 'track')
        limit = request.args.get('limit', 10, type=int)
        
        if not q:
            return jsonify({'error': 'Search query is required'}), 400
        
        limit = max(1, min(50, limit))
        if search_type not in ['track', 'artist', 'album', 'playlist']:
            search_type = 'track'
        
        spotify = auth_manager.get_spotify_client(token_info)
        results = spotify.search(q=q, type=search_type, limit=limit)
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get track recommendations based on seed tracks/artists/genres
    Query parameters:
    - seed_tracks: comma-separated track IDs
    - seed_artists: comma-separated artist IDs
    - seed_genres: comma-separated genres
    - limit: number of recommendations (default: 20, max: 100)
    """
    try:
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        seed_tracks = request.args.get('seed_tracks', '').split(',') if request.args.get('seed_tracks') else None
        seed_artists = request.args.get('seed_artists', '').split(',') if request.args.get('seed_artists') else None
        seed_genres = request.args.get('seed_genres', '').split(',') if request.args.get('seed_genres') else None
        limit = request.args.get('limit', 20, type=int)
        
        limit = max(1, min(100, limit))
        
        if not any([seed_tracks, seed_artists, seed_genres]):
            return jsonify({'error': 'At least one seed parameter is required'}), 400
        
        spotify = auth_manager.get_spotify_client(token_info)
        results = spotify.recommendations(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            seed_genres=seed_genres,
            limit=limit
        )
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Debug mode - change to False for production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
