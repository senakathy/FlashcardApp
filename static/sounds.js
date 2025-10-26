// ============================================================================
// SOUND EFFECTS USING WEB AUDIO API
// This file creates sound effects without needing any audio files
// All sounds are generated programmatically using JavaScript
// ============================================================================

// Create an audio context - this is what generates all our sounds
// Different browsers use different names, so we try both
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioContext = new AudioContext();  // This is our sound generator

// ============================================================================
// SOFT BUTTON CLICK SOUND
// Plays a gentle "tap" sound when you click buttons
// ============================================================================
function playClickSound() {
    // Create an oscillator - this makes a continuous tone
    const oscillator = audioContext.createOscillator();
    
    // Create a gain node - this controls the volume
    const gainNode = audioContext.createGain();
    
    // Connect them: oscillator -> gain -> speakers
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);  // destination = your speakers
    
    // Set the frequency (pitch) to 1000 Hz - a pleasant high tone
    oscillator.frequency.value = 1000;
    
    // Use a sine wave for a pure, smooth sound
    oscillator.type = 'sine';
    
    // Set volume to very quiet (0.08 out of 1.0)
    gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
    
    // Fade out quickly to 0.01 over 0.05 seconds
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
    
    // Start playing the sound now
    oscillator.start(audioContext.currentTime);
    
    // Stop after 0.05 seconds (50 milliseconds)
    oscillator.stop(audioContext.currentTime + 0.05);
}

// ============================================================================
// CARD FLIP SOUND (WHOOSH)
// Plays when you flip a flashcard to see the other side
// ============================================================================
function playFlipSound() {
    // Calculate how many samples we need for 0.15 seconds
    const bufferSize = audioContext.sampleRate * 0.15;
    
    // Create a buffer to hold our sound data
    // 1 channel (mono), bufferSize samples, at the audio context's sample rate
    const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
    
    // Get access to the actual audio data
    const data = buffer.getChannelData(0);
    
    // Fill the buffer with white noise that fades out
    // This creates the "whoosh" sound
    for (let i = 0; i < bufferSize; i++) {
        // Random value between -1 and 1 (white noise)
        // Multiply by a fade-out curve (starts loud, gets quiet)
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, 2);
    }
    
    // Create a source that will play our buffer
    const noise = audioContext.createBufferSource();
    
    // Create a filter to shape the sound
    const filter = audioContext.createBiquadFilter();
    
    // Create gain to control volume
    const gainNode = audioContext.createGain();
    
    // Set our buffer as the source
    noise.buffer = buffer;
    
    // Connect: noise source -> filter -> gain -> speakers
    noise.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Use a bandpass filter - only lets through middle frequencies
    filter.type = 'bandpass';
    
    // Start at 2000 Hz (high pitch)
    filter.frequency.setValueAtTime(2000, audioContext.currentTime);
    
    // Sweep down to 500 Hz (lower pitch) over 0.15 seconds
    // This creates the "swooshing" effect
    filter.frequency.exponentialRampToValueAtTime(500, audioContext.currentTime + 0.15);
    
    // Q value controls how "focused" the filter is
    filter.Q.value = 1;
    
    // Set volume to 0.12 (quiet)
    gainNode.gain.setValueAtTime(0.12, audioContext.currentTime);
    
    // Fade out to almost silent over 0.15 seconds
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
    
    // Start playing now
    noise.start(audioContext.currentTime);
    
    // Stop after 0.15 seconds
    noise.stop(audioContext.currentTime + 0.15);
}

// ============================================================================
// CARD SWIPE SOUND (SWOOSH)
// Plays when you navigate to the previous/next flashcard
// Similar to flip sound but slightly different to differentiate
// ============================================================================
function playSwipeSound() {
    // Calculate buffer size for 0.2 seconds (slightly longer than flip)
    const bufferSize = audioContext.sampleRate * 0.2;
    
    // Create a buffer to hold sound data
    const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
    
    // Get the audio data array
    const data = buffer.getChannelData(0);
    
    // Fill with white noise that fades out more gradually
    for (let i = 0; i < bufferSize; i++) {
        // Random noise with a different fade curve (power of 2.5)
        // This makes it sound slightly different from the flip
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, 2.5);
    }
    
    // Create audio nodes
    const noise = audioContext.createBufferSource();
    const filter = audioContext.createBiquadFilter();
    const gainNode = audioContext.createGain();
    
    // Set the buffer
    noise.buffer = buffer;
    
    // Connect the chain: noise -> filter -> gain -> speakers
    noise.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Use bandpass filter
    filter.type = 'bandpass';
    
    // Start at 1500 Hz (slightly lower than flip sound)
    filter.frequency.setValueAtTime(1500, audioContext.currentTime);
    
    // Sweep down to 400 Hz over 0.2 seconds
    filter.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.2);
    
    // Slightly more focused filter
    filter.Q.value = 1.5;
    
    // Set volume
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    
    // Smooth fade out
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
    
    // Start playing
    noise.start(audioContext.currentTime);
    
    // Stop after 0.2 seconds
    noise.stop(audioContext.currentTime + 0.2);
}

// ============================================================================
// ADD CLICK SOUNDS TO ALL BUTTONS
// This function finds all buttons on the page and adds click sounds to them
// ============================================================================
function addButtonSounds() {
    // Find all button elements and elements with class 'btn'
    document.querySelectorAll('button, .btn').forEach(button => {
        // For each button found, add a click event listener
        button.addEventListener('click', function(e) {
            // When clicked, play the soft click sound
            playClickSound();
        });
    });
}

// ============================================================================
// INITIALIZE SOUNDS WHEN PAGE LOADS
// Makes sure sounds are set up as soon as the page is ready
// ============================================================================

// Check if the page is still loading
if (document.readyState === 'loading') {
    // If still loading, wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', addButtonSounds);
} else {
    // If already loaded, add button sounds immediately
    addButtonSounds();
}
