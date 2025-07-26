window.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const spinner = document.getElementById('spinner');

    // When the response is present, hide spinner and enable button
    if (window.hasResponse) {
        if (spinner) spinner.style.display = 'none';
        if (analyzeBtn) analyzeBtn.disabled = false;
    }

    // Show spinner and disable button on form submit
    if (analyzeBtn && spinner) {
        analyzeBtn.form.addEventListener('submit', function() {
            analyzeBtn.disabled = true;
            spinner.style.display = 'inline-block';
        });
    }
});

// Show spinner on form submit
const form = document.getElementById('upload-form');
const spinner = document.getElementById('spinner');
form.addEventListener('submit', () => {
    spinner.style.display = 'inline-block';
    document.getElementById('analyze-btn').disabled = true;
});

// Camera stream controls
const img = document.getElementById('camera-stream');
const startBtn = document.getElementById('start-camera');
const stopBtn = document.getElementById('stop-camera');

function startCamera() {
    img.style.display = 'block';
    startBtn.disabled = true;
    stopBtn.disabled = false;
    img.src = "/camera";
}

function stopCamera() {
    img.src = "";
    img.style.display = 'none';
    startBtn.disabled = false;
    stopBtn.disabled = true;
}

startBtn.addEventListener('click', startCamera);
stopBtn.addEventListener('click', stopCamera);