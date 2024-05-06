// Function to remove or hide images based on detected card names
function updateGallery(detectedCards) {
    // Get all the images in the gallery
    const images = document.querySelectorAll('.gallery img');

    // Iterate through each image
    images.forEach(image => {
        // Check if the alt attribute of the image matches any of the detected card names
        if (detectedCards.includes(image.alt)) {
            // If a match is found, remove or hide the image
            image.style.display = 'none'; // You can use 'none' to hide or 'remove()' to remove from the DOM
        } else {
            // If no match is found, make sure the image is visible
            image.style.display = 'block'; // Display the image
        }
    });
}

// Function to fetch detected cards from Flask server and update the gallery
function fetchDetectedCardsAndUpdateGallery() {
    fetch('http://localhost:5001/cards')
        .then(response => response.json()) // Parse JSON response
        .then(data => {
            // Assign the detected cards to the global variable
            detectedCards = data;

            // Log the detected cards to the console
            console.log('Detected cards:', detectedCards);

            // Update the gallery based on the detected cards
            updateGallery(detectedCards);
        })
        .catch(error => console.error('Error fetching detected cards:', error));
}

// Call the fetchDetectedCardsAndUpdateGallery function every second
setInterval(fetchDetectedCardsAndUpdateGallery, 1000);


document.querySelectorAll('.card-carousel').forEach(function(carousel) {
    const cards = carousel.querySelector('.cards');
    const cardWidth = carousel.querySelector('.card').offsetWidth;
    let position = 0;

    carousel.querySelector('.prev').addEventListener('click', function() {
        position += cardWidth;
        position = Math.min(position, 0);
        cards.style.transform = `translateX(${position}px)`;
    });

    carousel.querySelector('.next').addEventListener('click', function() {
        position -= cardWidth;
        const maxPosition = -((cards.children.length - 1) * cardWidth);
        position = Math.max(position, maxPosition);
        cards.style.transform = `translateX(${position}px)`;
    });
});
