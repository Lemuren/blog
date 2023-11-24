function fetchComments() {
    fetch('/api/comment')
        .then(response => response.text())
        .then(data => {
            document.getElementById('comment-section').innerHTML = data;
        })
        .catch(error => console.error('Error fetching comments:', error));
}
