function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // If the requested file is index.html
    if (uri.endsWith('index.html')) {
        // Generate a random number between 0 and 1
        var randomNumber = Math.random();

        // If the random number is less than 0.5, change the requested file to index2.html
        if (randomNumber < 0.5) {
            request.uri = uri.replace('index.html', 'index2.html');
        }
    }

    return request;
}