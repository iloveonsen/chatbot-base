document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const lineHeight = parseFloat(window.getComputedStyle(userInput).lineHeight);
    const maxLines = 5;
    const maxHeight = lineHeight * maxLines;

    userInput.addEventListener('input', function() {
        this.style.height = 'auto'; // Reset height to recalculate
        if (this.scrollHeight <= maxHeight) {
            this.style.height = `${Math.max(this.scrollHeight, lineHeight)}px`;
            this.style.overflowY = 'hidden'; // Hide scrollbar when content is within maxLines
        } else {
            this.style.height = `${maxHeight}px`;
            this.style.overflowY = 'scroll'; // Show scrollbar when content exceeds maxLines
        }
    });
});