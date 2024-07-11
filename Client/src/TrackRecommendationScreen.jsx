import React, { useState } from "react";
import axios from "axios";

export default function TrackRecommendationScreen({ playlistId }) {
  const [recommendations, setRecommendations] = useState("ASLDKAS");
  const getTrackRecommendations = async () => {
    try {
      const response = await axios.get(
        `http://localhost:5000/api/get_track_recommendations/${encodeURIComponent(
          playlistId
        )}`
      );
      console.log(response);
      // setRecommendations(response.data);
    } catch (error) {
      console.error("Error getting track recommendations:", error);
    }
  };
  return <button onClick={getTrackRecommendations}>{playlistId}</button>;
}
