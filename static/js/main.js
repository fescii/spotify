// Initialize the visualization using Chart.js
let currentChart = null;

function initializeApp() {
    // Add event listeners to all select elements
    const moodSelect = document.getElementById('mood-selection');
    const visualizationSelect = document.getElementById('visualization-type');
    const sortingSelect = document.getElementById('sorting-method');

    // Add change event listeners
    [moodSelect, visualizationSelect, sortingSelect].forEach(select => {
        if (select) {
            select.addEventListener('change', updateAnalysis);
        }
    });
    
    // Initial analysis
    updateAnalysis();
}

async function updateAnalysis() {
    const mood = document.getElementById('mood-selection')?.value || 'happy';
    const visualizationType = document.getElementById('visualization-type')?.value || 'audioFeatures';
    const sortMethod = document.getElementById('sorting-method')?.value || 'popularity';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mood,
                visualizationType,
                sortMethod
            })
        });
        
        const data = await response.json();
        updateVisualization(data.visualizationData, visualizationType);
        updateTrackList(data.tracks);
    } catch (error) {
        console.error('Error fetching analysis:', error);
    }
}

function updateVisualization(data, type) {
    const chartContainer = document.getElementById('analysis-results');
    if (!chartContainer) return;

    let canvas = chartContainer.querySelector('canvas');

    // If canvas doesn't exist, create it
    if (!canvas) {
        canvas = document.createElement('canvas');
        chartContainer.appendChild(canvas);
    }

    // Destroy existing chart if it exists
    if (currentChart) {
        currentChart.destroy();
    }

    // Create a new chart based on the visualization type
    if (type === 'audioFeatures') {
        currentChart = createAudioFeaturesChart(canvas, data);
    } else if (type === 'genreDistribution') {
        currentChart = createGenreDistributionChart(canvas, data);
    } else if (type === 'topSongs') {
        currentChart = createTopSongsChart(canvas, data);
    }
}

function updateTrackList(tracks) {
    const trackList = document.getElementById('trackList');
    if (!trackList) return;

    trackList.innerHTML = tracks.map(track => `
        <div class="p-4 bg-white rounded-lg shadow">
            <h3 class="font-semibold">${track.name}</h3>
            <p class="text-gray-600">${track.artist}</p>
            <div class="mt-2 text-sm text-gray-500">
                Popularity: ${track.popularity} | Energy: ${track.energy.toFixed(2)} | 
                Danceability: ${track.danceability.toFixed(2)}
            </div>
        </div>
    `).join('');
}

// Chart creation functions
function createAudioFeaturesChart(ctx, data) {
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Audio Features',
                data: Object.values(data),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function createGenreDistributionChart(ctx, data) {
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(data),  // Genre names
            datasets: [{
                data: Object.values(data),  // Genre counts
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                    '#FF9F40', '#B4E1FF', '#FF6384', '#C9CBCF', '#4B5000'
                ],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
            }
        }
    });
}


function createTopSongsChart(ctx, data) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(track => track.name),  // Song names
            datasets: [{
                label: 'Popularity',
                data: data.map(track => track.popularity),  // Popularity scores
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: 'Top Songs' } },
                y: { beginAtZero: true, title: { display: true, text: 'Popularity' } }
            }
        }
    });
}


// Initialize the app when the document is loaded
document.addEventListener('DOMContentLoaded', initializeApp);