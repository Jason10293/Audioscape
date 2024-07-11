import React from "react";

export default function ClickablePlaylistCover({
  playlistCoverArtURL,
  width,
  onClick,
  index,
}) {
  return (
    <div>
      <img
        onClick={() => onClick(index)}
        src={playlistCoverArtURL}
        width={width}
        className="cursor-pointer"
      />
    </div>
  );
}
