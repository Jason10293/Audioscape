import SpotifyAuth from "./SpotifyAuth";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PlaylistSelection from "./PlaylistSelection";
export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SpotifyAuth />} />
        <Route path="/PlaylistSelection" element={<PlaylistSelection />} />
      </Routes>
    </Router>
  );
}
