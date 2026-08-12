const CLIENT_ID =
  import.meta.env.VITE_SPOTIFY_CLIENT_ID ||
  "";

const REDIRECT_URI =
  import.meta.env.VITE_SPOTIFY_REDIRECT_URI ||
  "http://127.0.0.1:5173/callback";

const ACCOUNTS_URL = "https://accounts.spotify.com";
const API_URL = "https://api.spotify.com/v1";

const STORAGE_KEYS = {
  verifier: "spotify_code_verifier",
  state: "spotify_auth_state",
  accessToken: "spotify_access_token",
  refreshToken: "spotify_refresh_token",
  expiresAt: "spotify_expires_at",
  scope: "spotify_scope",
};

function randomString(length = 64) {
  const chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~";

  const values = crypto.getRandomValues(new Uint8Array(length));

  return Array.from(values)
    .map((value) => chars[value % chars.length])
    .join("");
}

async function sha256(value: string) {
  return crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(value)
  );
}

function base64UrlEncode(buffer: ArrayBuffer) {
  return btoa(
    String.fromCharCode(...new Uint8Array(buffer))
  )
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=/g, "");
}

async function createCodeChallenge(verifier: string) {
  const hash = await sha256(verifier);
  return base64UrlEncode(hash);
}

export async function login() {
  if (!CLIENT_ID) {
    throw new Error(
      "Missing VITE_SPOTIFY_CLIENT_ID environment variable."
    );
  }

  const verifier = randomString(64);
  const challenge = await createCodeChallenge(verifier);
  const state = randomString(32);

  sessionStorage.setItem(STORAGE_KEYS.verifier, verifier);
  sessionStorage.setItem(STORAGE_KEYS.state, state);

  /*
   * Only request scopes that the application actually needs.
   *
   * This starter uses profile information only.
   */
  const scope = "user-read-private user-read-email";

  const params = new URLSearchParams({
    response_type: "code",
    client_id: CLIENT_ID,
    scope,
    redirect_uri: REDIRECT_URI,
    state,
    code_challenge_method: "S256",
    code_challenge: challenge,
  });

  window.location.href =
    `${ACCOUNTS_URL}/authorize?${params.toString()}`;
}

async function exchangeCode(code: string) {
  const verifier = sessionStorage.getItem(STORAGE_KEYS.verifier);

  if (!verifier) {
    throw new Error(
      "Spotify PKCE verifier is missing. Please authenticate again."
    );
  }

  const response = await fetch(`${ACCOUNTS_URL}/api/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      client_id: CLIENT_ID,
      grant_type: "authorization_code",
      code,
      redirect_uri: REDIRECT_URI,
      code_verifier: verifier,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error_description ||
        data.error ||
        "Spotify authorization failed."
    );
  }

  saveTokens(data);

  sessionStorage.removeItem(STORAGE_KEYS.verifier);
  sessionStorage.removeItem(STORAGE_KEYS.state);

  return data.access_token;
}

function saveTokens(data: {
  access_token: string;
  expires_in: number;
  refresh_token?: string;
  scope?: string;
}) {
  localStorage.setItem(
    STORAGE_KEYS.accessToken,
    data.access_token
  );

  localStorage.setItem(
    STORAGE_KEYS.expiresAt,
    String(Date.now() + data.expires_in * 1000)
  );

  if (data.refresh_token) {
    localStorage.setItem(
      STORAGE_KEYS.refreshToken,
      data.refresh_token
    );
  }

  if (data.scope) {
    localStorage.setItem(STORAGE_KEYS.scope, data.scope);
  }
}

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem(
    STORAGE_KEYS.refreshToken
  );

  if (!refreshToken) {
    throw new Error("NO_REFRESH_TOKEN");
  }

  const response = await fetch(`${ACCOUNTS_URL}/api/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: refreshToken,
      client_id: CLIENT_ID,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    if (data.error === "invalid_grant") {
      logout();

      throw new Error("REAUTH_REQUIRED");
    }

    throw new Error(
      data.error_description ||
        data.error ||
        "Spotify token refresh failed."
    );
  }

  saveTokens(data);

  return data.access_token;
}

async function getAccessToken() {
  const accessToken = localStorage.getItem(
    STORAGE_KEYS.accessToken
  );

  const expiresAt = Number(
    localStorage.getItem(STORAGE_KEYS.expiresAt) || "0"
  );

  /*
   * Refresh slightly before expiration.
   */
  if (
    accessToken &&
    expiresAt > Date.now() + 60_000
  ) {
    return accessToken;
  }

  return refreshAccessToken();
}

export async function handleCallback() {
  const params = new URLSearchParams(
    window.location.search
  );

  const error = params.get("error");
  const code = params.get("code");
  const returnedState = params.get("state");

  if (error) {
    throw new Error(
      `Spotify authorization failed: ${error}`
    );
  }

  if (!code) {
    return null;
  }

  const savedState = sessionStorage.getItem(
    STORAGE_KEYS.state
  );

  if (!returnedState || returnedState !== savedState) {
    throw new Error(
      "Spotify authorization state validation failed."
    );
  }

  return exchangeCode(code);
}

export function logout() {
  Object.values(STORAGE_KEYS).forEach((key) => {
    localStorage.removeItem(key);
    sessionStorage.removeItem(key);
  });
}

export function isLoggedIn() {
  return Boolean(
    localStorage.getItem(STORAGE_KEYS.accessToken) ||
      localStorage.getItem(STORAGE_KEYS.refreshToken)
  );
}

async function spotifyRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  retryCount = 0
): Promise<T> {
  const token = await getAccessToken();

  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      ...options,
      headers: {
        Authorization: `Bearer ${token}`,
        ...(options.headers || {}),
      },
    }
  );

  if (response.ok) {
    /*
     * Some successful Spotify endpoints return no body.
     */
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  let errorData: any = null;

  try {
    errorData = await response.json();
  } catch {
    // Response did not contain JSON.
  }

  /*
   * Access token expired or became invalid.
   */
  if (response.status === 401 && retryCount === 0) {
    localStorage.removeItem(STORAGE_KEYS.accessToken);
    localStorage.removeItem(STORAGE_KEYS.expiresAt);

    return spotifyRequest<T>(
      endpoint,
      options,
      retryCount + 1
    );
  }

  /*
   * Spotify rate limit.
   *
   * Retry-After is expressed in seconds.
   */
  if (response.status === 429 && retryCount < 3) {
    const retryAfterHeader =
      response.headers.get("Retry-After");

    const retryAfter = retryAfterHeader
      ? Number(retryAfterHeader)
      : Math.pow(2, retryCount);

    const delay =
      Math.max(retryAfter, 1) * 1000;

    await new Promise((resolve) =>
      setTimeout(resolve, delay)
    );

    return spotifyRequest<T>(
      endpoint,
      options,
      retryCount + 1
    );
  }

  const spotifyMessage =
    errorData?.error?.message ||
    errorData?.error_description ||
    errorData?.error ||
    `Spotify API request failed with HTTP ${response.status}.`;

  throw new Error(spotifyMessage);
}

/*
 * User profile
 */
export async function getCurrentUser() {
  return spotifyRequest("/me");
}

/*
 * Search
 *
 * IMPORTANT:
 * Keep the requested types explicit instead of assuming
 * Spotify response fields.
 */
export async function searchSpotify(
  query: string,
  types = "track,artist,album",
  limit = 20
): Promise<any> {
  const params = new URLSearchParams({
    q: query,
    type: types,
    limit: String(limit),
  });

  return spotifyRequest(
    `/search?${params.toString()}`
  );
}

/*
 * Current playback information.
 */
export async function getCurrentlyPlaying() {
  return spotifyRequest(
    "/me/player"
  );
}

/*
 * User's recently played tracks.
 */
export async function getRecentlyPlayed(
  limit = 20
): Promise<any> {
  const params = new URLSearchParams({
    limit: String(limit),
  });

  return spotifyRequest(
    `/me/player/recently-played?${params.toString()}`
  );
}