/**
 * Main Application Logic
 * Handles UI interactions and integration with Spotify API
 */

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    console.log('🎵 Spotify Clone initialized');
    
    // Setup event listeners
    setupSearchListener();
    setupPlaylistInteraction();
    setupPlayerControls();
    setupSidebarNavigation();
    setupActivityListeners();
    
    // Load initial data
    loadPlaylistData();
    loadFriendActivity();
}

// ==================== SEARCH ==================== 
function setupSearchListener() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', debounce((e: Event) => {
        const query = (e.target as HTMLInputElement).value;
        if (query.length > 2) {
            performSearch(query);
        }
    }, 500));
}

function performSearch(query: string) {
    console.log(`Searching for: ${query}`);
    // TODO: Integrate with backend search API
    // fetch(`/api/search?q=${encodeURIComponent(query)}`)
}

// ==================== PLAYLIST INTERACTION ====================
function setupPlaylistInteraction() {
    const playButton = document.querySelector('.btn-play');
    const followButton = document.querySelector('.btn-follow');
    const downloadButton = document.querySelector('.btn-download');
    
    playButton?.addEventListener('click', () => {
        console.log('▶ Playing playlist');
        // TODO: Integrate with playback API
    });
    
    followButton?.addEventListener('click', () => {
        console.log('♡ Following playlist');
        followButton?.classList.toggle('following');
    });
    
    downloadButton?.addEventListener('click', () => {
        console.log('⬇ Downloading playlist');
    });
}

// ==================== PLAYER CONTROLS ====================
function setupPlayerControls() {
    const playMainBtn = document.querySelector('.btn-play-main');
    const buttons = document.querySelectorAll('.btn-control');
    const prevBtn = buttons.length > 0 ? buttons[0] : null;
    const nextBtn = buttons.length > 2 ? buttons[2] : null;
    
    playMainBtn?.addEventListener('click', togglePlayback);
    prevBtn?.addEventListener('click', playPrevious);
    nextBtn?.addEventListener('click', playNext);
    
    // Setup progress bar
    const progressBar = document.querySelector('.progress-bar');
    progressBar?.addEventListener('click', (e) => {
        const percent = (e as MouseEvent).offsetX / (progressBar as HTMLElement).offsetWidth;
        seekTrack(percent);
    });
    
    // Setup volume
    const volumeBar = document.querySelector('.volume-bar');
    volumeBar?.addEventListener('click', (e) => {
        const percent = (e as MouseEvent).offsetX / (volumeBar as HTMLElement).offsetWidth;
        setVolume(percent);
    });
}

function togglePlayback() {
    const btn = document.querySelector('.btn-play-main') as HTMLElement | null;
    if (btn && btn.textContent === '⏵') {
        btn.textContent = '⏸';
        console.log('▶ Playing');
    } else if (btn) {
        btn.textContent = '⏵';
        console.log('⏸ Paused');
    }
}

function playPrevious() {
    console.log('⏮ Previous track');
}

function playNext() {
    console.log('⏭ Next track');
}

function seekTrack(percent: number) {
    const progress = document.querySelector('.progress-fill') as HTMLElement;
    if (progress) {
        progress.style.width = `${percent * 100}%`;
    }
    console.log(`Seeking to ${(percent * 100).toFixed(1)}%`);
}

function setVolume(percent: number) {
    const volumeFill = document.querySelector('.volume-fill') as HTMLElement;
    if (volumeFill) {
        volumeFill.style.width = `${percent * 100}%`;
    }
    console.log(`Volume: ${(percent * 100).toFixed(0)}%`);
}

// ==================== SIDEBAR NAVIGATION ====================
function setupSidebarNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const nav = btn.textContent?.trim();
            console.log(`Navigating to: ${nav}`);
        });
    });
    
    const playlistItems = document.querySelectorAll('.playlist-item');
    playlistItems.forEach(item => {
        item.addEventListener('click', () => {
            playlistItems.forEach(p => p.classList.remove('active'));
            item.classList.add('active');
            const playlist = item.textContent?.trim();
            console.log(`Loading playlist: ${playlist}`);
        });
    });
}

// ==================== ACTIVITY LISTENERS ====================
function setupActivityListeners() {
    const activityItems = document.querySelectorAll('.activity-item');
    activityItems.forEach(item => {
        const htmlItem = item as HTMLElement;
        htmlItem.addEventListener('click', () => {
            const name = htmlItem.querySelector('.activity-name')?.textContent;
            console.log(`Viewing activity from: ${name}`);
        });
        
        htmlItem.addEventListener('mouseenter', () => {
            htmlItem.style.transform = 'translateX(4px)';
        });
        
        htmlItem.addEventListener('mouseleave', () => {
            htmlItem.style.transform = 'translateX(0)';
        });
    });
    
    // Heart button
    const heartBtn = document.querySelector('.btn-heart') as HTMLElement | null;
    heartBtn?.addEventListener('click', () => {
        if (heartBtn && heartBtn.textContent === '♡') {
            heartBtn.textContent = '♥';
            heartBtn.style.color = 'var(--accent-orange)';
            console.log('♥ Liked song');
        } else if (heartBtn) {
            heartBtn.textContent = '♡';
            heartBtn.style.color = 'var(--text-secondary)';
            console.log('♡ Removed from liked');
        }
    });
}

// ==================== DATA LOADING ====================
function loadPlaylistData() {
    // TODO: Replace with actual API data
    const playlistData = {
        title: 'Drive Loud',
        description: 'Forget the traffic stress.',
        creator: 'Spotify',
        stats: '50 songs, 2 hr 46 min',
        image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=200&h=200&fit=crop'
    };
    
    document.getElementById('playlistTitle')!.textContent = playlistData.title;
    document.getElementById('playlistDescription')!.textContent = playlistData.description;
    document.getElementById('playlistCreator')!.textContent = playlistData.creator;
    document.getElementById('playlistStats')!.textContent = playlistData.stats;
    
    const imageOverlay = document.querySelector('.image-overlay') as HTMLElement;
    if (imageOverlay) {
        imageOverlay.style.backgroundImage = `url('${playlistData.image}')`;
    }
}

function loadFriendActivity() {
    // TODO: Replace with actual API data
    const activities = [
        {
            name: 'Pollen Merida',
            action: 'Liked a song',
            detail: 'Of Course',
            avatar: 'https://i.pravatar.cc/32?img=2'
        },
        {
            name: 'Rosie Clever',
            action: 'Created a playlist',
            detail: 'American Daydream',
            avatar: 'https://i.pravatar.cc/32?img=3'
        },
        {
            name: 'Koray Savaş',
            action: 'Liked a song',
            detail: 'This Is Mucism Opera',
            avatar: 'https://i.pravatar.cc/32?img=4'
        },
        {
            name: 'Didem Satian',
            action: 'Added to playlist',
            detail: 'Pictures Of You',
            avatar: 'https://i.pravatar.cc/32?img=5'
        }
    ];
    
    const activityList = document.getElementById('activityList');
    if (activityList) {
        activityList.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <img src="${activity.avatar}" alt="${activity.name}">
                <div class="activity-info">
                    <p class="activity-name">${activity.name}</p>
                    <p class="activity-song">${activity.action}</p>
                    <p class="activity-detail">${activity.detail}</p>
                </div>
            </div>
        `).join('');
        
        setupActivityListeners();
    }
}

// ==================== UTILITY FUNCTIONS ====================
function debounce(func: Function, wait: number) {
    let timeout: ReturnType<typeof setTimeout>;
    return function executedFunction(...args: any[]) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== KEYBOARD SHORTCUTS ====================
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault();
        togglePlayback();
    }
    
    if (e.code === 'ArrowRight') {
        playNext();
    }
    
    if (e.code === 'ArrowLeft') {
        playPrevious();
    }
});

// ==================== THEME TOGGLE ====================
function setupTheme() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (isDark) {
        document.documentElement.style.colorScheme = 'dark';
    }
}

setupTheme();

console.log('✅ Application ready');
