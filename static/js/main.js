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