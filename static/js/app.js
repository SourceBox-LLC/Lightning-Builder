//Javascript to handle ...
document.getElementById('providerSelect').addEventListener('change', function() {
    var selectedModel = this.options[this.selectedIndex].text;
    var modelCard = document.getElementById('modelCard');
    var modelText = document.getElementById('modelText');
    var addTools = document.getElementById('addTools');
    var addScenarios = document.getElementById('addPrompt');

    if (selectedModel !== "Select Model") {
        modelText.textContent = "Selected Model: " + selectedModel; // Update text
        modelCard.style.display = 'block'; // Show the card
        addTools.style.display = 'block'; // Show the Add Tools section
        addScenarios.style.display = 'block'; // Show the Add Scenarios section
    } else {
        modelCard.style.display = 'none'; // Hide the card if no model is selected
        addTools.style.display = 'none'; // Hide the Add Tools section
        addScenarios.style.display = 'none'; // Hide the Add Scenarios section
    }
});


// JavaScript to handle toolkit selection
document.getElementById('toolSelect').addEventListener('change', function() {
    var selectedToolkit = this.options[this.selectedIndex].text;
    var toolkitCard = document.getElementById('toolkitCard');
    var toolkitText = document.getElementById('toolkitText');

    if (selectedToolkit !== "Select Tool") {
        toolkitText.textContent = "Selected Toolkit: " + selectedToolkit; // Update text
        toolkitCard.style.display = 'block'; // Show the toolkit card
    } else {
        toolkitCard.style.display = 'none'; // Hide the toolkit card if no toolkit is selected
    }
});


// JavaScript to handle prompt submission
document.getElementById('promptText').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevents the default action of the Enter key

        var promptText = this.value.trim();
        var selectedToolkits = [];
        var rightColumn = document.querySelector('.right-column'); // Select the right column

        // Collect selected toolkits
        document.querySelectorAll('input[type="checkbox"]:checked').forEach(function(checkbox) {
            selectedToolkits.push(checkbox.value);
        });

        if (promptText && selectedToolkits.length > 0 && selectedToolkits.length <= 3) {
            // Show the right column
            rightColumn.style.display = 'block';

            // Create a new paragraph element to display the prompt
            var promptDisplay = document.createElement('p');
            promptDisplay.textContent = "Prompt: " + promptText + " (using " + selectedToolkits.join(', ') + ")";
            rightColumn.querySelector('.card-body').appendChild(promptDisplay);
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Array to store selected toolkits
    var selectedToolkits = [];

    // Handle toolkit selection
    document.getElementById('toolSelect').addEventListener('change', function() {
        var selectedToolkit = this.options[this.selectedIndex].text;
        var toolkitCard = document.getElementById('toolkitCard');
        var toolkitText = document.getElementById('toolkitText');

        if (selectedToolkit !== "Select Tool") {
            toolkitText.textContent = "Selected Toolkit: " + selectedToolkit;
            toolkitCard.style.display = 'block';
        } else {
            toolkitCard.style.display = 'none';
        }
    });

    // Handle adding toolkit
    document.getElementById('addToolkitButton').addEventListener('click', function() {
        var selectedToolkit = document.getElementById('toolkitText').textContent.replace('Selected Toolkit: ', '');
        var rightColumn = document.querySelector('.right-column');

        if (selectedToolkit !== "None" && !selectedToolkits.includes(selectedToolkit) && selectedToolkits.length < 3) {
            selectedToolkits.push(selectedToolkit);

            rightColumn.style.display = 'block';

            var toolkitCard = document.createElement('div');
            toolkitCard.className = 'card mt-2';
            var toolkitCardBody = document.createElement('div');
            toolkitCardBody.className = 'card-body';
            toolkitCardBody.textContent = "Toolkit: " + selectedToolkit;
            toolkitCard.appendChild(toolkitCardBody);
            rightColumn.querySelector('.card-body').appendChild(toolkitCard);

            document.getElementById('toolSelect').selectedIndex = 0;
            document.getElementById('toolkitCard').style.display = 'none';
            document.getElementById('toolkitText').textContent = "Selected Toolkit: None";
        }
    });

    // Handle prompt submission
    document.getElementById('promptText').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();

            var promptText = this.value.trim();
            var rightColumn = document.querySelector('.right-column');

            if (promptText && selectedToolkits.length > 0) {
                rightColumn.style.display = 'block';

                var promptDisplay = document.createElement('p');
                promptDisplay.textContent = "Prompt: " + promptText + " (using " + selectedToolkits.join(', ') + ")";
                rightColumn.querySelector('.card-body').appendChild(promptDisplay);

                this.value = ''; // Clear the textarea after submission
            }
        }
    });

    // Handle configuration generation
    document.getElementById('generateConfigButton').addEventListener('click', function() {
        const selectedModel = document.getElementById('modelText').textContent.replace('Selected Model: ', '');
        const selectedToolkits = Array.from(document.querySelectorAll('.right-column .card-body div'))
                                      .map(div => div.textContent.replace('Toolkit: ', ''));
        const agentPrompt = document.getElementById('promptText').value.trim();

        fetch('/generate-config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                selected_model: selectedModel,
                selected_toolkits: selectedToolkits,
                agent_prompt: agentPrompt
            })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
    });
});
