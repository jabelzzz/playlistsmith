// Main UI state for the browser-only Spotify workflow.
const loginBtn = document.getElementById('btn-login')
const logoutBtn = document.getElementById('btn-logout')
const playlistsGrid = document.getElementById('playlists')
const authStatus = document.getElementById('auth-status')
const menuPanel = document.getElementById('menu-panel')
const selectedPlaylistTitle = document.getElementById('selected-playlist-title')
const sortStatus = document.getElementById('sort-status')
const playlistCount = document.getElementById('playlist-count')
const methodButtons = Array.from(document.querySelectorAll('.method-btn'))
const orderSelect = document.getElementById('sort-direction')

const state = {
  token: sessionStorage.getItem('spotify_token') || null,
  selectedPlaylist: null,
  playlists: []
}

function updateAuthUi() {
  const isLoggedIn = Boolean(state.token)
  loginBtn?.classList.toggle('hidden', isLoggedIn)
  logoutBtn?.classList.toggle('hidden', !isLoggedIn)
  authStatus.textContent = isLoggedIn
    ? 'Signed in. Loading your playlists…'
    : 'Connect your Spotify account to browse playlists.'
}

function updateSelectionUi() {
  if (state.selectedPlaylist) {
    menuPanel?.classList.remove('hidden')
    selectedPlaylistTitle.textContent = `Selected: ${state.selectedPlaylist.name}`
    sortStatus.textContent = ''
  } else {
    menuPanel?.classList.add('hidden')
    selectedPlaylistTitle.textContent = 'Select a playlist to see available methods.'
    sortStatus.textContent = ''
  }
}

// Render the playlists as cards with cover art and selection state.
function renderPlaylists(items) {
  state.playlists = items
  playlistsGrid.innerHTML = ''
  playlistCount.textContent = `${items.length} playlist${items.length === 1 ? '' : 's'}`

  if (!items.length) {
    playlistsGrid.innerHTML = '<div class="empty-state">No playlists available yet.</div>'
    return
  }

  items.forEach((playlist) => {
    const card = document.createElement('button')
    card.type = 'button'
    card.className = `playlist-card${state.selectedPlaylist?.id === playlist.id ? ' selected' : ''}`

    const image = document.createElement('img')
    image.alt = `${playlist.name} cover`
    image.src = playlist.image_url || 'https://placehold.co/200x200/181818/ffffff?text=Playlist'

    const info = document.createElement('div')
    info.className = 'playlist-info'
    const title = document.createElement('h3')
    title.textContent = playlist.name
    const meta = document.createElement('p')
    meta.textContent = `${playlist.tracks} tracks`

    info.appendChild(title)
    info.appendChild(meta)
    card.appendChild(image)
    card.appendChild(info)
    card.addEventListener('click', () => {
      state.selectedPlaylist = playlist
      renderPlaylists(state.playlists)
      updateSelectionUi()
    })

    playlistsGrid.appendChild(card)
  })
}

// Load the current user's playlists and show them immediately after login.
async function listPlaylists() {
  const token = sessionStorage.getItem('spotify_token')
  if (!token) {
    alert('Please login first')
    return
  }

  state.token = token
  authStatus.textContent = 'Loading playlists...'
  const res = await fetch('/playlists', {
    headers: { Authorization: `Bearer ${token}` }
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    authStatus.textContent = 'Unable to load playlists.'
    alert(`Error listing playlists: ${err.detail || res.status}`)
    return
  }

  const data = await res.json()
  const items = data.items || []
  renderPlaylists(items)
  updateSelectionUi()

  if (items.length) {
    authStatus.textContent = `All playlists loaded (${items.length}).`
  } else {
    authStatus.textContent = 'No playlists were found for this account.'
  }
}

// Reorder the selected playlist without deleting any tracks; only the order changes.
async function sortPlaylist(playlistId, method, direction) {
  const token = sessionStorage.getItem('spotify_token')
  if (!token) {
    alert('Please login first')
    return
  }

  const res = await fetch('/sort', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ playlist_id: playlistId, method, direction })
  })

  const data = await res.json().catch(() => null)
  if (!res.ok) {
    sortStatus.textContent = `Sort failed: ${data?.detail || res.status}`
    return
  }

  sortStatus.textContent = `Reordered ${state.selectedPlaylist?.name || 'the selected playlist'} by ${method} (${direction}). No tracks were removed.`
}

// Remove duplicate tracks while preserving the first copy of each song.
async function removeDuplicates(playlistId) {
  const token = sessionStorage.getItem('spotify_token')
  if (!token) {
    alert('Please login first')
    return
  }

  const res = await fetch('/remove_duplicates', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ playlist_id: playlistId })
  })

  const data = await res.json().catch(() => null)
  if (!res.ok) {
    sortStatus.textContent = `Cleanup failed: ${data?.detail || res.status}`
    return
  }

  sortStatus.textContent = `Removed duplicate tracks from ${state.selectedPlaylist?.name || 'the selected playlist'}.`
}

loginBtn?.addEventListener('click', () => {
  window.location.href = '/login'
})

logoutBtn?.addEventListener('click', () => {
  sessionStorage.removeItem('spotify_token')
  state.token = null
  state.selectedPlaylist = null
  state.playlists = []
  renderPlaylists([])
  updateAuthUi()
  updateSelectionUi()
  authStatus.textContent = 'Signed out. Login again to continue.'
})

methodButtons.forEach((button) => {
  button.addEventListener('click', async () => {
    if (!state.selectedPlaylist) {
      sortStatus.textContent = 'Select a playlist first.'
      return
    }
    const direction = orderSelect?.value || 'descending'
    if (button.dataset.method === 'remove_duplicates') {
      await removeDuplicates(state.selectedPlaylist.id)
      return
    }
    await sortPlaylist(state.selectedPlaylist.id, button.dataset.method, direction)
  })
})

function initializeApp() {
  updateAuthUi()
  updateSelectionUi()
  if (state.token) {
    void listPlaylists()
  }
}

initializeApp()

