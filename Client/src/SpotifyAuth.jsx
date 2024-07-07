import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function SpotifyAuth() {
  const navigate = useNavigate();

  useEffect(() => {
    // Check if there's a token in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("access_token");

    if (token) {
      navigate("/playlistSelection");
    }
  }, [navigate]);

  const handleLogin = () => {
    window.location.href = "http://localhost:5000/login";
  };

  return (
    <div className="bg-spotify-black h-screen flex flex-wrap items-center justify-center">
      <header>
        <button
          className="text-spotify-black border-spotify-green border-solid border-2 p-2 bg-spotify-green rounded-md"
          onClick={handleLogin}
        >
          Log in with Spotify
        </button>
      </header>
    </div>
  );
}
