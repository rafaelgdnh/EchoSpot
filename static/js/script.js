// Function to enable/disable sliders and hide/show output based on checkbox state
function setupSlider(checkboxId, sliderId, outputId) {
    document.getElementById(checkboxId).addEventListener('change', function(e) {
        var slider = document.getElementById(sliderId);
        var output = document.getElementById(outputId);
        slider.disabled = !this.checked;
        output.style.visibility = this.checked ? 'visible' : 'hidden';
    });

    // Update the slider input listener to format the output
    document.getElementById(sliderId).addEventListener('input', function(e) {
        document.getElementById(outputId).value = parseFloat(e.target.value).toFixed(2);
    });

    // Initialize slider and output visibility based on checkbox state at page load
    var checkbox = document.getElementById(checkboxId);
    var slider = document.getElementById(sliderId);
    var output = document.getElementById(outputId);
    slider.disabled = !checkbox.checked;
    output.style.visibility = checkbox.checked ? 'visible' : 'hidden';

    // Initialize the output value formatted to two decimal places
    output.value = parseFloat(slider.value).toFixed(2);
}

let currentStep = 1;
const maxSteps = 10; // Including the final "Generate Playlist" step

function showCurrentStep() {
    // Hide all steps
    for (let i = 1; i <= maxSteps; i++) {
        let step = document.getElementById(`step${i}`);
        if (step) {
            step.style.display = i === currentStep ? 'block' : 'none';
        }
    }
}

function updateSummary() {
    const summaryList = document.getElementById('selectionSummary');
    summaryList.innerHTML = ''; // Clear existing summary items

    const playlistName = document.getElementById('playlist_name').value;
    const trackCount = document.getElementById('limit').value;
    const genre = document.getElementById('seed_genres').value;
    const genreText = genre === 'random' ? 'Random Genre' : genre;

    summaryList.innerHTML += `<li>Playlist Name: ${playlistName}</li>`;
    summaryList.innerHTML += `<li>Number of Tracks: ${trackCount}</li>`;
    summaryList.innerHTML += `<li>Genre: ${genreText}</li>`;

    // Add only enabled features to the summary
    addFeatureToSummary('enable_danceability', 'target_danceability', 'Danceability');
    addFeatureToSummary('enable_energy', 'target_energy', 'Energy');
    addFeatureToSummary('enable_acousticness', 'target_acousticness', 'Acousticness');
    addFeatureToSummary('enable_speechiness', 'target_speechiness', 'Speechiness');
    addFeatureToSummary('enable_liveness', 'target_liveness', 'Liveness');
    addFeatureToSummary('enable_loudness', 'target_loudness', 'Loudness');
}

function addFeatureToSummary(checkboxId, sliderId, featureName) {
    const checkbox = document.getElementById(checkboxId);
    if (checkbox && checkbox.checked) {
        const value = document.getElementById(sliderId).value;
        const summaryList = document.getElementById('selectionSummary');
        summaryList.innerHTML += `<li>${featureName}: ${value}</li>`;
    }
}


// Adjusted nextStep function to include input validation
function nextStep() {
    // Perform validation only on specific steps
    if (currentStep === 1) {
        const playlistName = document.getElementById('playlist_name').value;
        if (!playlistName) {
            document.getElementById('playlistNameWarning').style.display = 'block';
            return; // Stop the function if validation fails
        } else {
            document.getElementById('playlistNameWarning').style.display = 'none';
        }
    } else if (currentStep === 2) {
        const trackCount = document.getElementById('limit').value;
        if (!trackCount || trackCount < 1 || trackCount > 50) { // Assuming trackCount limits
            document.getElementById('trackCountWarning').style.display = 'block';
            return; // Stop the function if validation fails
        } else {
            document.getElementById('trackCountWarning').style.display = 'none';
        }
    }

    // Update and show the summary before the final step
    if (currentStep === maxSteps - 1) {
        updateSummary();
    }

    if (currentStep < maxSteps) {
        currentStep++;
        showCurrentStep();
    }
}

// Adjusted prevStep function to hide warnings when going back
function prevStep() {
    if (currentStep > 1) {
        // Hide any validation warnings
        document.getElementById('playlistNameWarning').style.display = 'none';
        document.getElementById('trackCountWarning').style.display = 'none';

        currentStep--;
        showCurrentStep();
    }
}

// Call setupSlider for each feature and show the current step
window.onload = function() {
    setupSlider('enable_danceability', 'target_danceability', 'danceability-output');
    setupSlider('enable_energy', 'target_energy', 'energy-output');
    setupSlider('enable_acousticness', 'target_acousticness', 'acousticness-output');
    setupSlider('enable_speechiness', 'target_speechiness', 'speechiness-output');
    setupSlider('enable_liveness', 'target_liveness', 'liveness-output');
    setupSlider('enable_loudness', 'target_loudness', 'loudness-output');
    showCurrentStep(); // Initialize to show the first step
};

