document.addEventListener('DOMContentLoaded', function() {
    // Array to store selected toolkits
    let selectedToolkits = [];
    console.log("Document loaded. Initial selected toolkits:", selectedToolkits);

    // Handle model selection
    document.getElementById('providerSelect').addEventListener('change', function() {
        var selectedModel = this.options[this.selectedIndex].text;
        console.log("Model selected:", selectedModel);
        var modelCard = document.getElementById('modelCard');
        var modelText = document.getElementById('modelText');
        var addTools = document.getElementById('addTools');
        var addScenarios = document.getElementById('addPrompt');

        if (selectedModel !== "Select Model") {
            modelText.textContent = "Selected Model: " + selectedModel;
            modelCard.style.display = 'block'; // Show the card
            addTools.style.display = 'block';  // Show the Add Tools section
            addScenarios.style.display = 'block';  // Show the Add Scenarios section
        } else {
            modelCard.style.display = 'none';  // Hide the card if no model is selected
            addTools.style.display = 'none';  // Hide the Add Tools section
            addScenarios.style.display = 'none';  // Hide the Add Scenarios section
        }
    });

    // Handle toolkit selection
    document.getElementById('toolSelect').addEventListener('change', function() {
        var selectedToolkit = this.options[this.selectedIndex].text;
        console.log("Toolkit selected:", selectedToolkit);
        var toolkitCard = document.getElementById('toolkitCard');
        var toolkitText = document.getElementById('toolkitText');

        if (selectedToolkit !== "Select Tool") {
            toolkitText.textContent = "Selected Toolkit: " + selectedToolkit;
            toolkitCard.style.display = 'block';  // Show the toolkit card
        } else {
            toolkitCard.style.display = 'none';  // Hide the toolkit card if no toolkit is selected
        }
    });

    // Handle adding toolkit (with no duplicates)
    document.getElementById('addToolkitButton').addEventListener('click', function() {
        var selectedToolkit = document.getElementById('toolkitText').textContent.replace('Selected Toolkit: ', '');
        console.log("Add toolkit button clicked. Toolkit to add:", selectedToolkit);
        var rightColumn = document.querySelector('.right-column');

        if (selectedToolkit !== "None" && !selectedToolkits.includes(selectedToolkit) && selectedToolkits.length < 3) {
            selectedToolkits.push(selectedToolkit);
            console.log("Toolkit added:", selectedToolkit, "Current toolkits:", selectedToolkits);

            rightColumn.style.display = 'block';

            // Clear previous content
            rightColumn.querySelector('.card-body').innerHTML = '';

            // Display all selected toolkits
            selectedToolkits.forEach(toolkit => {
                var toolkitCard = document.createElement('div');
                toolkitCard.className = 'card mt-2';
                var toolkitCardBody = document.createElement('div');
                toolkitCardBody.className = 'card-body';
                toolkitCardBody.textContent = "Toolkit: " + toolkit;
                toolkitCard.appendChild(toolkitCardBody);
                rightColumn.querySelector('.card-body').appendChild(toolkitCard);
            });

            // Reset selection and hide toolkit card
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
            console.log("Prompt submitted:", promptText);
            var rightColumn = document.querySelector('.right-column');

            if (promptText && selectedToolkits.length > 0) {
                rightColumn.style.display = 'block';

                var promptDisplay = document.createElement('p');
                promptDisplay.textContent = "Prompt: " + promptText + " (using " + selectedToolkits.join(', ') + ")";
                rightColumn.querySelector('.card-body').appendChild(promptDisplay);
            }
        }
    });

    // Handle configuration generation
    document.getElementById('generateConfigButton').addEventListener('click', function() {
        const selectedModel = document.getElementById('modelText').textContent.replace('Selected Model: ', '');
        const agentPrompt = document.getElementById('promptText').value.trim(); // Capture the prompt text
        const agentName = document.getElementById('agentName').value.trim(); // Capture the agent name
        const agentDescription = document.getElementById('agentDescription').value.trim(); // Capture the agent description

        console.log("Generating configuration with model:", selectedModel, "toolkits:", selectedToolkits, "prompt:", agentPrompt, "name:", agentName, "description:", agentDescription);

        // Ensure the prompt is included in the configuration
        fetch('/generate-config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                selected_model: selectedModel,
                selected_toolkits: selectedToolkits, // No duplicates here
                agent_prompt: agentPrompt, // Include the prompt in the request
                agent_name: agentName, // Include the agent name
                agent_description: agentDescription // Include the agent description
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Configuration generated successfully:", data);
            alert(data.message);

            // Reset values after configuration is generated successfully
            document.getElementById('modelText').textContent = 'Selected Model: None';
            document.getElementById('promptText').value = ''; // Clear the prompt input
            document.getElementById('agentName').value = ''; // Clear the agent name input
            document.getElementById('agentDescription').value = ''; // Clear the agent description input
            selectedToolkits.length = 0; // Clear the selected toolkits array

            // Reset the toolkits display section
            const rightColumn = document.querySelector('.right-column');
            const cardBody = rightColumn.querySelector('.card-body');
            cardBody.innerHTML = ''; // Clear toolkit cards from the right column
            rightColumn.style.display = 'none'; // Hide the right column

            // Hide the model card and Add Tools section
            document.getElementById('modelCard').style.display = 'none';
            document.getElementById('addTools').style.display = 'none';
            document.getElementById('addPrompt').style.display = 'none';

            // Reset toolkit selection
            document.getElementById('toolSelect').selectedIndex = 0;
            document.getElementById('toolkitCard').style.display = 'none';
            document.getElementById('toolkitText').textContent = 'Selected Toolkit: None';
        })
        .catch(error => console.error('Error:', error));
    });

});
