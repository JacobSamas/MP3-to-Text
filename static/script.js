document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('lyrics').textContent = data.lyrics || data.error;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('copyButton').addEventListener('click', function() {
    const lyrics = document.getElementById('lyrics').textContent;
    navigator.clipboard.writeText(lyrics).then(() => {
        alert('Lyrics copied to clipboard!');
    }).catch(err => {
        alert('Failed to copy lyrics:', err);
    });
});
