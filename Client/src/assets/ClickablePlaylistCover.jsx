import React from "react";

export default function ClickablePlaylistCover({ playlistCoverArtURL, width }) {
  return (
    <div>
      <img src={playlistCoverArtURL} width={width} />
    </div>
  );
}
