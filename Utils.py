genres = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues",
          "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical",
          "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco",
          "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french",
          "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock",
          "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian",
          "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop",
          "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno",
          "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop",
          "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b",
          "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad",
          "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul",
          "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop",
          "turkish", "work-out", "world-music"]

category_to_id = {'New Releases': '0JQ5DAqbMKFz6FAsUtgAab', 'Pop': '0JQ5DAqbMKFEC4WFtoNRpw', 'Hip-Hop': '0JQ5DAqbMKFQ00XGBls6ym', 'Rock': '0JQ5DAqbMKFDXXwE9BDJAr', 'Latin': '0JQ5DAqbMKFxXaXKP7zcDp', 'Charts': '0JQ5DAudkNjCgYMM0TZXDw', 'Dance/Electronic': '0JQ5DAqbMKFHOzuVTgTizF', 'Mood': '0JQ5DAqbMKFzHmL4tf05da', 'Indie': '0JQ5DAqbMKFCWjUTdzaG0e', 'Workout': '0JQ5DAqbMKFAXlCG6QvYQ4', 'Discover': '0JQ5DAtOnAEpjOgUKwXyxj', 'Country': '0JQ5DAqbMKFKLfwjuJMoNC', 'R&B': '0JQ5DAqbMKFEZPnFQSFB1T', 'K-pop': '0JQ5DAqbMKFGvOw3O4nLAf', 'Chill': '0JQ5DAqbMKFFzDl7qN9Apr', 'Sleep': '0JQ5DAqbMKFCuoRTxhYWow', 'Party': '0JQ5DAqbMKFA6SOHvT3gck', 'At Home': '0JQ5DAqbMKFx0uLQR2okcc', 'Decades': '0JQ5DAqbMKFIVNxQgRNSg0', 'Love': '0JQ5DAqbMKFAUsdyVjCQuL', 'Metal': '0JQ5DAqbMKFDkd668ypn6O', 'Jazz': '0JQ5DAqbMKFAJ5xb0fwo9m', 'Trending': '0JQ5DAqbMKFQIL0AXnG5AK', 'Wellness': '0JQ5DAqbMKFLb2EqgLtpjC', 'Anime': '0JQ5DAqbMKFziKOShCi009', 'Gaming': '0JQ5DAqbMKFCfObibaOZbv', 'Folk & Acoustic': '0JQ5DAqbMKFy78wprEpAjl', 'Focus': '0JQ5DAqbMKFCbimwdOYlsl', 'Soul': '0JQ5DAqbMKFIpEuaCnimBj', 'Kids & Family': '0JQ5DAqbMKFFoimhOqWzLB', 'Classical': '0JQ5DAqbMKFPrEiAOxgac3', 'TV & Movies': '0JQ5DAqbMKFOzQeOmemkuw', 'Instrumental': '0JQ5DAqbMKFRieVZLLoo9m', 'Punk': '0JQ5DAqbMKFAjfauKLOZiv', 'Ambient': '0JQ5DAqbMKFLjmiZRss79w', 'Netflix': '0JQ5DAqbMKFEOEBCABAxo9', 'Blues': '0JQ5DAqbMKFQiK2EHwyjcU', 'Cooking & Dining': '0JQ5DAqbMKFRY5ok2pxXJ0', 'Alternative': '0JQ5DAqbMKFFtlLYUHv8bT', 'Travel': '0JQ5DAqbMKFAQy4HL4XU2D', 'Caribbean': '0JQ5DAqbMKFObNLOHydSW8', 'Afro': '0JQ5DAqbMKFNQ0fGp4byGU', 'GLOW': '0JQ5DAqbMKFGnsSfvg90Wo', 'Songwriters': '0JQ5DAqbMKFSCjnQr8QZ3O', 'Nature & Noise': '0JQ5DAqbMKFI3pNLtYMD9S', 'Funk & Disco': '0JQ5DAqbMKFFsW9N8maB6z', 'League of Legends': '0JQ5DAqbMKFLYQVFHcXMae', 'Spotify Singles': '0JQ5DAqbMKFDBgllo2cUIN', 'Summer': '0JQ5DAqbMKFLVaM30PMBm4', 'EQUAL': '0JQ5DAqbMKFPw634sFwguI', 'RADAR': '0JQ5DAqbMKFOOxftoKZxod', 'Fresh Finds': '0JQ5DAqbMKFImHYGo3eTSg', 'Tastemakers': '0JQ5DAqbMKFRKBHIxJ5hMm'}



def parse_params_to_dict(input_str):
    # Initial cleanup: remove curly braces and split by newline to get individual entries
    entries = input_str.strip("{}").split(",\n")

    # Initialize an empty dictionary to store the parsed key-value pairs
    result_dict = {}

    for entry in entries:
        # Split each entry by the first colon to separate key and value
        key, value = entry.split(": ", 1)

        # Remove any leading or trailing whitespace and quotes from the key
        key = key.strip().strip('"')

        # Try converting numerical values to float or int, and strip quotes from strings
        try:
            # Attempt to convert to a float first
            value = float(value)
            # If the value is actually an integer (no decimal part), convert it to int
            if value.is_integer():
                value = int(value)
        except ValueError:
            # If conversion fails, it's a string, so remove leading/trailing whitespace and quotes
            value = value.strip().strip('"')

        # Add the parsed key-value pair to the result dictionary
        result_dict[key] = value

    return result_dict


def extract_nearest_neighbours_input(params_dict):
    knn_keys = [
        "target_acousticness", "target_danceability",
        "target_energy", "target_instrumentalness", "target_valence"
    ]

    knn_values_dict = {}
    for key, value in params_dict.items():
        if key in knn_keys:
            key_name = key.replace("target_", "")
            knn_values_dict[key_name] = value

    return knn_values_dict


def validate_and_fix_dict(params_dict, add_artists=True):
    spotify_params = [
        "min_acousticness", "max_acousticness",
        "min_danceability", "max_danceability",
        "min_energy", "max_energy", "max_instrumentalness",
        "min_liveness", "seed_artists", "seed_tracks"
    ]

    # Remove any keys that are not in the list of valid Spotify parameters
    for key in list(params_dict.keys()):
        if key not in spotify_params:
            del params_dict[key]

    if not add_artists:
        if "seed_artists" in params_dict:
            del params_dict["seed_artists"]
    elif "seed_artists" in params_dict:
        if isinstance(params_dict["seed_artists"], list):
            params_dict["seed_artists"] = ",".join(params_dict["seed_artists"])

    if "seed_tracks" in params_dict:
        if isinstance(params_dict["seed_tracks"], list):
            params_dict["seed_tracks"] = ",".join(params_dict["seed_tracks"])

def limit_dict_seeds_number(params_dict, add_artists=True):
    # validates that no more than a total of 4 seed tracks and artists are given
    seed_artists = []
    seed_tracks = []
    if "seed_artists" in params_dict:
        if isinstance(params_dict["seed_artists"], str):
            seed_artists = params_dict["seed_artists"].split(",")
        else:
            seed_artists = params_dict["seed_artists"]

    if "seed_tracks" in params_dict:
        if isinstance(params_dict["seed_tracks"], str):
            seed_tracks = params_dict["seed_tracks"].split(",")
        else:
            seed_tracks = params_dict["seed_tracks"]

    if not add_artists:
        if "seed_artists" in params_dict:
            del params_dict["seed_artists"]
    elif "seed_artists" in params_dict:
        if len(seed_artists) > 2:
            params_dict["seed_artists"] = ",".join(seed_artists[:2])

    if "seed_tracks" in params_dict:
        if add_artists:
            if len(seed_tracks) > 2:
                params_dict["seed_tracks"] = ",".join(seed_tracks[:2])
        else:
            if len(seed_tracks) > 5:
                params_dict["seed_tracks"] = ",".join(seed_tracks[:5])



def correct_audio_values_in_place(predict_audio_features):
    audio_values_diff = {
        'danceability': 0.009000000000000008,
        'energy': -0.04799999999999999,
        'loudness': -0.054000000000000714,
        'speechiness': -0.0009999999999999974,
        'acousticness': 0.000969,
        'instrumentalness': 3.4200000000000003e-06,
        'liveness': -0.016249999999999994,
        'valence': -0.049000000000000016,
        'tempo': -5.667500000000004}

    audio_values_diff = {
        'danceability': 0.009000000000000008, 'energy': -0.04799999999999999,
        'loudness': -0.054000000000000714, 'speechiness': -0.0009999999999999974,
        'acousticness': 0.000969, 'instrumentalness': 3.4200000000000003e-06,
        'liveness': -0.016249999999999994, 'valence': -0.049000000000000016,
        'tempo': -5.667500000000004
    }

    for key, value in predict_audio_features.items():
        plain_key = key.replace("min_", "").replace("max_", "").replace("target_", "")
        if plain_key in audio_values_diff:
            adjusted_value = value + audio_values_diff[plain_key]
            adjusted_value = max(0, min(adjusted_value, 1))
            predict_audio_features[key] = float(adjusted_value)
