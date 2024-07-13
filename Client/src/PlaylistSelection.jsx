import React from "react";
import playlistData from "../../user_playlists.json";
import ClickablePlaylistCover from "./ClickablePlaylistCover";
import { useNavigate } from "react-router-dom";

export default function PlaylistSelection({ selectPlaylistOnClick }) {
  let navigate = useNavigate();
  const routeChange = () => {
    navigate("/TrackRecommendationScreen");
  };
  const onClick = (index) => {
    selectPlaylistOnClick(index);
    routeChange();
  };
  const playlistCoverArtURLS = playlistData.items
    .filter(
      (playlist) =>
        playlist.images[0].url !==
        "https://lexicon-assets.spotifycdn.com/DJ-Beta-CoverArt-300.jpg"
    )
    .map((playlist) => playlist.images[0].url);
  console.log(playlistCoverArtURLS);
  return (
    <div className="bg-spotify-black min-h-screen p-10 px-44 flex flex-col items-center justify-center">
      <header className="text-spotify-green text-4xl mb-10 font-roboto">
        Select a Playlist
      </header>
      <div className="flex flex-wrap justify-center gap-32">
        {playlistCoverArtURLS.map((url, index) => (
          <div
            key={index}
            className="transform transition duration-300 ease-in-out hover:-translate-y-2"
          >
            <ClickablePlaylistCover
              index={index}
              onClick={() => onClick(index)}
              playlistCoverArtURL={url}
              width={200}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
