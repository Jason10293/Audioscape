import React, { useState, useEffect } from "react";
import axios from "axios";

function SpotifyAuth() {
  const [playlists, setPlaylists] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    window.location.href = "http://localhost:5000/login";
  };

  return (
    <div>
      <header>
        <h1>Spotify Playlist Viewer</h1>
        <button onClick={handleLogin}>Log in with Spotify</button>
      </header>
    </div>
  );
}

export default SpotifyAuth;
