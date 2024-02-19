genres = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical", "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"]


def parse_to_dict(input_str):
    # Initial cleanup: remove curly braces and split by newline to get individual entries
    entries = input_str.strip("{}").split(",\n")

    # Initialize an empty dictionary to store the parsed key-value pairs
    result_dict = {}

    for entry in entries:
        # Split each entry by the first colon to separate key and value
        key, value = entry.split(": ", 1)

        # Remove any leading or trailing whitespace and quotes from the key
        key = key.strip().strip('"')
        spotify_params = [
            "min_acousticness", "max_acousticness",
            "min_danceability", "max_danceability",
            "min_energy", "max_energy", "max_instrumentalness",
            "min_liveness", "seed_artists", "seed_tracks"
        ]

        if key not in spotify_params:
            continue

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