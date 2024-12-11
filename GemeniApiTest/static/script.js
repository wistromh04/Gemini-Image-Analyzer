const form = document.getElementById('upload-form');
const responseDiv = document.getElementById('response');

form.onsubmit = async function (event) {
    event.preventDefault(); 
    const formData = new FormData(form);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.error) {
            responseDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        } else {
            responseDiv.innerHTML = `<p><strong>AI Response:</strong><br>${data.response}</p>`;
        }
    } catch (error) {
        responseDiv.innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
    }
};
