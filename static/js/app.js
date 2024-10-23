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
            checkCompileContent(); // Check content after model selection
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

    // Initially hide and disable the download button
    const downloadButton = document.querySelector('#downloadTemplate button');
    downloadButton.style.display = 'none';
    downloadButton.disabled = true;

    // Elements for spinner and waiting message
    const spinner = document.getElementById('spinner');
    const waitingMessage = document.getElementById('waitingMessage');

    // Function to enable and show the download button
    function enableDownloadButton() {
        downloadButton.style.display = 'block';
        downloadButton.disabled = false;
    }

    // Function to hide spinner and waiting message
    function hideSpinnerAndMessage() {
        if (spinner) spinner.style.display = 'none';
        if (waitingMessage) waitingMessage.style.display = 'none';
    }

    // Function to check and hide spinner/message if content is present
    function checkCompileContent() {
        const modelText = document.getElementById('modelText').textContent;
        if (modelText !== 'Selected Model: None') {
            hideSpinnerAndMessage();
        }
    }

    // Handle configuration generation
    document.getElementById('generateConfigButton').addEventListener('click', function() {
        const selectedModel = document.getElementById('modelText').textContent.replace('Selected Model: ', '');
        const agentPrompt = document.getElementById('promptText').value.trim();
        const agentName = document.getElementById('agentName').value.trim();
        const agentDescription = document.getElementById('agentDescription').value.trim();

        // Validate required fields
        if (selectedModel === 'None') {
            alert('Please select a model.');
            return;
        }
        if (!agentPrompt) {
            alert('Please enter a prompt.');
            return;
        }
        if (!agentName) {
            alert('Please enter an agent name.');
            return;
        }
        if (!agentDescription) {
            alert('Please enter an agent description.');
            return;
        }

        console.log("Generating configuration with model:", selectedModel, "toolkits:", selectedToolkits, "prompt:", agentPrompt, "name:", agentName, "description:", agentDescription);

        // Ensure the prompt is included in the configuration
        fetch('/generate-config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                selected_model: selectedModel,
                selected_toolkits: selectedToolkits,
                agent_prompt: agentPrompt,
                agent_name: agentName,
                agent_description: agentDescription
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Configuration generated successfully:", data);
            alert(data.message);

            // Reset values after configuration is generated successfully
            document.getElementById('modelText').textContent = 'Selected Model: None';
            document.getElementById('promptText').value = '';
            document.getElementById('agentName').value = '';
            document.getElementById('agentDescription').value = '';
            selectedToolkits.length = 0;

            // Reset the toolkits display section
            const rightColumn = document.querySelector('.right-column');
            const cardBody = rightColumn.querySelector('.card-body');
            cardBody.innerHTML = '';
            rightColumn.style.display = 'none';

            // Hide the model card and Add Tools section
            document.getElementById('modelCard').style.display = 'none';
            document.getElementById('addTools').style.display = 'none';
            document.getElementById('addPrompt').style.display = 'none';

            // Reset toolkit selection
            document.getElementById('toolSelect').selectedIndex = 0;
            document.getElementById('toolkitCard').style.display = 'none';
            document.getElementById('toolkitText').textContent = 'Selected Toolkit: None';

            // Show the assembly area
            document.getElementById('assemblyHeader').style.display = 'block';
            document.getElementById('assemblyCode').style.display = 'block';

            // Automatically fetch and display the configuration
            fetch('/display-config')
                .then(response => response.json())
                .then(configData => {
                    if (configData.error) {
                        alert(configData.error);
                    } else {
                        const yamlString = `
build:
  model: ${configData.build.model}
  prompt: ${configData.build.prompt}
  toolkits:
  ${configData.build.toolkits.map(toolkit => `  - ${toolkit}`).join('\n')}
project:
  description: ${configData.project.description}
  name: ${configData.project.name}
  version: ${configData.project.version}
                        `;

                        document.getElementById('configContent').textContent = yamlString;
                        document.getElementById('buildFileHeader').style.display = 'block';
                        document.getElementById('buildFileContent').style.display = 'block';
                    }
                })
                .catch(error => console.error('Error fetching configuration:', error));

            // Trigger the assemble-config route
            fetch('/assemble-config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(assembleData => {
                console.log("Template assembled successfully:", assembleData);
                alert(assembleData.message);

                document.getElementById('assemblyCode').innerHTML = `<pre>${assembleData.final_template}</pre>`;
                document.getElementById('assemblyRequirementsHeader').style.display = 'block';
                document.getElementById('assemblyRequirements').style.display = 'block';
                document.getElementById('assemblyRequirements').innerHTML = `<pre>${assembleData.requirements}</pre>`;
            })
            .catch(error => console.error('Error during assembly:', error));

            // Enable the download button after successful configuration generation
            enableDownloadButton();

            // Check and hide spinner/message if content is present
            checkCompileContent();
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle download agent button click
    document.getElementById('downloadTemplate').addEventListener('click', function() {
        console.log("Downloading agent...");

        // Trigger the download-agent route
        fetch('/download-agent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                return response.blob();  // Convert the response to a Blob
            } else {
                throw new Error('Failed to download agent');
            }
        })
        .then(blob => {
            // Create a link element to download the file
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'agent_template.zip';  // Set the default file name
            document.body.appendChild(a);
            a.click();  // Programmatically click the link to trigger the download
            a.remove();  // Remove the link from the document
            window.URL.revokeObjectURL(url);  // Release the object URL

            // Trigger the delete-files route
            return fetch('/delete-files', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        })
        .then(response => {
            if (response.ok) {
                console.log('Files and directory deleted successfully.');
            } else {
                throw new Error('Failed to delete files and directory');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle upload configuration button click
    const uploadButton = document.getElementById('uploadConfigurationButton');
    if (uploadButton) {
        uploadButton.addEventListener('click', function() {
            const uploadConfigSection = document.getElementById('uploadConfigSection');
            if (uploadConfigSection) {
                uploadConfigSection.style.display = 'block'; // Show the textarea and submit button

                // Disable all input fields except the textarea and submit button
                const inputs = document.querySelectorAll('input, textarea, button');
                inputs.forEach(input => {
                    if (input !== document.getElementById('configTextarea') && input !== document.getElementById('submitConfigButton')) {
                        input.disabled = true;
                    }
                });
            } else {
                console.error('Element with ID "uploadConfigSection" not found.');
            }
        });
    } else {
        console.error('Element with ID "uploadConfigurationButton" not found.');
    }

    // Handle submit configuration button click
    const submitButton = document.getElementById('submitConfigButton');
    if (submitButton) {
        submitButton.addEventListener('click', function() {
            const configContent = document.getElementById('configTextarea').value.trim();
            console.log("Config content:", configContent);

            if (configContent) {
                console.log("Submitting custom configuration...");

                // Use /custom-config instead of /generate-config
                fetch('/custom-config', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ config: configContent })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Configuration processed successfully:", data);
                    alert(data.message);

                    // Reset values after configuration is processed successfully
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

                    // Show the assembly area
                    document.getElementById('assemblyHeader').style.display = 'block'; // Show "Assembly" header
                    document.getElementById('assemblyCode').style.display = 'block';   // Show the container

                    // Fetch and display the configuration
                    fetch('/display-config')
                        .then(response => response.json())
                        .then(configData => {
                            if (configData.error) {
                                alert(configData.error);
                            } else {
                                // Directly display the configuration data
                                document.getElementById('configContent').textContent = JSON.stringify(configData, null, 2); // Use <pre> for formatting
                                document.getElementById('buildFileHeader').style.display = 'block'; // Show header
                                document.getElementById('buildFileContent').style.display = 'block'; // Show content
                            }
                        })
                        .catch(error => console.error('Error fetching configuration:', error));

                    // Trigger the assemble-config route
                    fetch('/assemble-config', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(assembleData => {
                        console.log("Template assembled successfully:", assembleData);
                        alert(assembleData.message);

                        // Display the final template code in the assemblyCode section
                        document.getElementById('assemblyCode').innerHTML = `<pre>${assembleData.final_template}</pre>`; // Use <pre> for formatting

                        // Display the generated requirements in the requirements section
                        document.getElementById('assemblyRequirementsHeader').style.display = 'block'; // Show requirements header
                        document.getElementById('assemblyRequirements').style.display = 'block'; // Show requirements section
                        document.getElementById('assemblyRequirements').innerHTML = `<pre>${assembleData.requirements}</pre>`; // Use <pre> for formatting
                    })
                    .catch(error => console.error('Error during assembly:', error));

                    // Enable the download button after successful configuration submission
                    enableDownloadButton();

                    // Check and hide spinner/message if content is present
                    checkCompileContent();
                })
                .catch(error => console.error('Error uploading configuration:', error));
            } else {
                alert('Please enter a valid configuration.');
            }
        });
    } else {
        console.error('Element with ID "submitConfigButton" not found.');
    }
});
