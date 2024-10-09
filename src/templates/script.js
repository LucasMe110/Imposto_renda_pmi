document.querySelectorAll('.code-input').forEach((input, index, inputs) => {
    input.addEventListener('input', (e) => {
        if (e.target.value.length === 1 && index < inputs.length - 1) {
            // Move to the next input when a digit is entered
            inputs[index + 1].focus();
        }
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && !e.target.value && index > 0) {
            // Move to the previous input when backspacing
            inputs[index - 1].focus();
        }
    });

    input.addEventListener('paste', (e) => {
        const pasteData = e.clipboardData.getData('text').slice(0, 4); // Get the first 4 characters
        pasteData.split('').forEach((char, i) => {
            inputs[i].value = char; // Fill each input with the pasted data
            if (i < inputs.length - 1) {
                inputs[i + 1].focus(); // Move focus to the next input after filling
            }
        });
        e.preventDefault(); // Prevent the default paste action
    });
});
