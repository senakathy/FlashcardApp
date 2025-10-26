// Sound effects using Web Audio API
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioContext = new AudioContext();

// Soft button click sound (like a gentle tap)
function playClickSound() {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Soft, pleasant frequency
    oscillator.frequency.value = 1000;
    oscillator.type = 'sine';
    
    // Very quiet and quick
    gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.05);
}

// Card flip sound (soft whoosh)
function playFlipSound() {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    const filter = audioContext.createBiquadFilter();
    
    oscillator.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Gentle rising tone
    oscillator.frequency.setValueAtTime(300, audioContext.currentTime);
    oscillator.frequency.linearRampToValueAtTime(500, audioContext.currentTime + 0.08);
    oscillator.type = 'sine';
    
    // Low-pass filter for warmth
    filter.type = 'lowpass';
    filter.frequency.value = 800;
    
    // Soft volume
    gainNode.gain.setValueAtTime(0.06, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.08);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.08);
}

// Card swipe sound (subtle swoosh)
function playSwipeSound() {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    const filter = audioContext.createBiquadFilter();
    
    oscillator.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Descending gentle tone
    oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.12);
    oscillator.type = 'sine';
    
    // Low-pass filter
    filter.type = 'lowpass';
    filter.frequency.value = 1000;
    
    // Very soft
    gainNode.gain.setValueAtTime(0.05, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.12);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.12);
}

// Add click sound to all buttons
function addButtonSounds() {
    document.querySelectorAll('button, .btn').forEach(button => {
        button.addEventListener('click', function(e) {
            playClickSound();
        });
    });
}

// Initialize sounds when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addButtonSounds);
} else {
    addButtonSounds();
}
