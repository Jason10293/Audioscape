import SpotifyAuth from "./SpotifyAuth";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PlaylistSelection from "./PlaylistSelection";
import playlistData from "../../user_playlists.json";
import TrackRecommendationScreen from "./TrackRecommendationScreen";
import { useState } from "react";
export default function App() {
  const [playlistId, setPlaylistId] = useState("");
  const selectPlaylistOnClick = (index) => {
    setPlaylistId(playlistData.items[index].id);
  };
  return (
    <Router>
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
