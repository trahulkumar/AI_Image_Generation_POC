document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt');
    const generateBtn = document.getElementById('generateBtn');
    const imageContainer = document.getElementById('imageContainer');
    const loader = document.getElementById('loader');
    const btnText = generateBtn.querySelector('.btn-text');

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }

        // UI Loading State
        generateBtn.disabled = true;
        btnText.style.display = 'none';
        loader.style.display = 'block';
        imageContainer.innerHTML = '<div class="placeholder-text">Generating...</div>';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt
                })
            });

            if (!response.ok) {
                throw new Error('Generation failed');
            }

            const data = await response.json();

            // Display Image
            const img = new Image();
            img.src = data.image;
            img.alt = prompt;

            img.onload = () => {
                imageContainer.innerHTML = '';
                imageContainer.appendChild(img);
            };

        } catch (error) {
            console.error('Error:', error);
            imageContainer.innerHTML = '<div class="placeholder-text" style="color: #ef4444;">Generation failed. Please try again.</div>';
        } finally {
            // Reset UI
            generateBtn.disabled = false;
            btnText.style.display = 'block';
            loader.style.display = 'none';
        }
    });
});
