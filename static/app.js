document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-btn');
    const searchInput = document.getElementById('search-input');
    const loadingState = document.getElementById('loading-state');
    const resultsContainer = document.getElementById('results-container');
    const latencyIndicator = document.getElementById('latency-indicator');
    const latencyTime = document.getElementById('latency-time');
    const micBtn = document.getElementById('mic-btn');
    const downloadBtn = document.getElementById('download-btn');
    const actionBar = document.getElementById('action-bar');

    searchBtn.addEventListener('click', performSearch);
    downloadBtn.addEventListener('click', () => window.print());
    
    // Allow 'Enter' key to trigger search if shift is not pressed
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            performSearch();
        }
    });

    // Web Speech API Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN'; // Indian English for better accuracy with local terms

        recognition.onstart = () => {
            micBtn.classList.add('recording');
            searchInput.placeholder = 'Listening...';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            searchInput.value = transcript;
            performSearch(); // Auto-search after speaking
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            micBtn.classList.remove('recording');
            searchInput.placeholder = 'e.g., We manufacture high-strength reinforced concrete for building columns...';
            alert('Microphone access denied or error occurred.');
        };

        recognition.onend = () => {
            micBtn.classList.remove('recording');
            searchInput.placeholder = 'e.g., We manufacture high-strength reinforced concrete for building columns...';
        };

        micBtn.addEventListener('click', () => {
            recognition.start();
        });
    } else {
        micBtn.style.display = 'none'; // Hide if browser doesn't support it
        console.warn('Speech Recognition API not supported in this browser.');
    }

    async function performSearch() {
        const query = searchInput.value.trim();
        if (!query) return;

        // UI updates for loading
        resultsContainer.innerHTML = '';
        latencyIndicator.classList.add('hidden');
        actionBar.classList.add('hidden');
        loadingState.classList.remove('hidden');

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }

            renderResults(data.results);
            
            // Update latency and show actions
            latencyTime.textContent = data.latency;
            latencyIndicator.classList.remove('hidden');
            actionBar.classList.remove('hidden');

        } catch (error) {
            console.error('Error fetching search results:', error);
            resultsContainer.innerHTML = `
                <div class="result-card glass-panel" style="border-color: #ef4444;">
                    <p style="color: #ef4444;">An error occurred while connecting to the engine. Ensure the FastAPI backend is running.</p>
                </div>
            `;
        } finally {
            loadingState.classList.add('hidden');
        }
    }

    function renderResults(results) {
        if (!results || results.length === 0) {
            resultsContainer.innerHTML = `<p style="color: var(--text-secondary); text-align: center;">No matching standards found.</p>`;
            return;
        }

        results.forEach((result, index) => {
            const card = document.createElement('div');
            card.className = 'result-card glass-panel';
            // Stagger animations
            card.style.animationDelay = `${index * 0.15}s`;
            
            card.innerHTML = `
                <div class="result-header">
                    <div class="result-title">
                        <h2>${result.id}</h2>
                        <h3>${result.title}</h3>
                    </div>
                    <div class="confidence-badge">
                        <i class="fa-solid fa-check"></i> ${result.confidence} Match
                    </div>
                </div>
                <div class="rationale-box">
                    <h4>Direct Extraction Rationale</h4>
                    <p>${result.rationale}...</p>
                </div>
            `;
            
            resultsContainer.appendChild(card);
        });
    }
});
