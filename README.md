# AudioScape
Audioscape analyzes your Spotify playlists and uses advanced algorithms to suggest new tracks you'll love, expanding your musical horizons with every use.

# How It's Made:

### **Technologies/Libraries used:** Python, Pandas, Sklearn, NumPy

This Python script is designed to interact with the Spotify API to analyze and recommend songs based on a user's playlist. It utilizes several technologies and libraries, including:

- **Spotipy:** A lightweight Python library for the Spotify Web API. It handles user authentication, making API requests, and parsing the responses. The script uses Spotipy to fetch tracks from a specified playlist, retrieve audio features for these tracks, and gather artist genres.
- **Pandas:** Used to manipulated the a dataset of Spotify songs in order to perform tasks such as data collection, data preperation, and feature engineering
- **NumPy:** NumPy was primarily used for numerical operations on arrays.
- **Scikit-learn:** Was used for feature scaling (MinMaxScaler), calculating cosine similarity between vectors, and transforming text data into a matrix of TF-IDF features (TfidfVectorizer).

### **Main Objectives:**

- **Authentication:** Uses Spotipy's SpotifyOAuth to authenticate with Spotify and gain access to a user's library.
- **Data Collection:** Fetches tracks from a specified Spotify playlist, including their audio features, and artist genres.
  
![image](https://github.com/Jason10293/Audioscape/assets/66051354/f3eafa32-9971-4bdf-af72-b18e84d739c0)

- **Data Preprocessing:** Cleans and transforms the data, including scaling numerical features, creating buckets for song popularity, one-hot encoding categorical features, and generating TF-IDF vectors for the genre of tracks
- **Feature Engineering:** Enhances the dataset with additional features, by dropping unnecessary features, and added more weight to songs that were more recenlty added to the playlist
- **Recommendation:** A user playlist vector is created by summing the values of a feature for all songs in a playlist giving an overall picture of the playlist. Then, the cosine similarity is calculated between the user's vector and the vectors from the Spotify playlist to find the most similar songs.

# Optimizations
- **Less API calls**: Instead of calling the Spotify API for every track I instead used a batch request, requesting the information of 100 songs or artists at a time thus reducing the number of API calls made. This change made the algorithm output the recommended songs more than 10x faster
- **Songs recently added have weight:** Recognizing that long playlists may contain older songs that don't accurately reflect a user's current taste, I implemented a feature that gives more weight to recently added songs when calculating the overall playlist vector. This ensures recommendations are aligned with the user's evolving musical preferences.
-** Term Frequency - Inverse Document Frequency (tf-idf)**: tf-idf in essence transforms text (track genres) into a numerical that can be interpreted by cosine similarity. a high tf-idf suggests that a track genre is a distinguishing track genre and would make sense that is should be more likely to appear in genre recommendation
  ![image](https://github.com/Jason10293/Audioscape/assets/66051354/972cbe2b-2809-4854-9654-c8424e07bdec)

