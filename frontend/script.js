// Declare a global variable to store detected cards
let detectedCards = [];

// Function to fetch detected cards from Flask server
function fetchDetectedCards() {
    fetch('http://localhost:5001/cards')
        .then(response => response.json()) // Parse JSON response
        .then(data => {
            // Assign the detected cards to the global variable
            detectedCards = data;

            // Log the detected cards to the console
            console.log('Detected cards:', detectedCards);

            // Do whatever you want with the detected cards here
        })
        .catch(error => console.error('Error fetching detected cards:', error));
}

// Call the fetchDetectedCards function every second
setInterval(fetchDetectedCards, 1000);
