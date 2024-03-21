document.getElementById("playlistForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Loading...";


    const formData = {};

    formData.event = document.getElementById("event").value;
    formData.music_genre = document.getElementById("music_genre").value;

    const mood = document.getElementById("mood").value;
    const decade = document.getElementById("decade").value;

    if (mood) formData.mood = mood;
    if (decade) formData.decade = decade;

    fetch("api/create_playlist", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
    })
    .then(async response => {
        const data = await response.json();
        if (!response.ok) {
            throw data;
        }
        return data;
    })
    .then(data => {
        // Handle successful response
            const playlistUrl = data.playlist_url;
            const link = document.createElement('a');
            link.href = playlistUrl;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.textContent = 'Open Playlist'; // Text to display for the link

            // Clear the resultDiv and append the link to it
            resultDiv.innerHTML = '';
            resultDiv.appendChild(link);
            })
    .catch(error => {
        if (error.detail && Array.isArray(error.detail)) {
            // Extract 'msg' from the first error detail (customize as needed)
            const errorMessage = error.detail.map(err => err.msg).join(", ");
            resultDiv.innerHTML = errorMessage;
        } else {
            // Generic error message for other types of errors
            resultDiv.innerHTML = "An error occurred. Please try again.";
        }
    });
});