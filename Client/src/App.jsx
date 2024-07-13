import SpotifyAuth from "./SpotifyAuth";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PlaylistSelection from "./PlaylistSelection";
import playlistData from "../../user_playlists.json";
import TrackRecommendationScreen from "./TrackRecommendationScreen";
import { useState } from "react";
export default function App() {
  const [playlistId, setPlaylistId] = useState("");
  const selectPlaylistOnClick = (index) => {
    setPlaylistId(
      playlistData.items.filter(
        (playlist) =>
          playlist.images[0].url !==
          "https://lexicon-assets.spotifycdn.com/DJ-Beta-CoverArt-300.jpg"
      )[index].id
    );
  };
  return (
    <Router>
      t
      <Routes>
        <Route path="/" element={<SpotifyAuth />} />
        <Route
          path="/PlaylistSelection"
          element={
            <PlaylistSelection
              selectPlaylistOnClick={(index) => selectPlaylistOnClick(index)}
            />
          }
        />
        <Route
          path="/TrackRecommendationScreen"
          element={<TrackRecommendationScreen playlistId={playlistId} />}
        ></Route>
      </Routes>
    </Router>
  );
}
