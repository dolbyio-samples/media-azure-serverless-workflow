---
description: "An example Media Workflow with Dolby.io presented at the 2021 Azure Serverless Conf"
languages:
- python
products:
- azure-functions
- azure-storage
- azure-cognitive-services
---

# Media Pipeline
This sample highlights how to use Azure functions and Dolby.io to create a media processing pipeline that transcribes and enhances input media.

## Getting Started

#### Prerequisites
- Install Python 3.8+
- Azure Storage Account
- Azure Speech-to-text service Account
- [Dolby.io Account, sign up for free](https://dolby.io/signup/)
- [ngrok account (only for local testing), sign up for free](https://ngrok.com/docs#http-local-https)

####  Params.json
- "cog_api_key": Azure Cognitive Services Speech-to-text API Key,
- "dolbyio_api_key": Dolby.io media API Key,
- "azure_api_key" : Azure storage account API key,

- "AZURE_ACC_NAME" : Azure storage account name,
- "AZURE_CONTAINER" : Azure storage container name,
- "AZURE_BLOB_OUTPUT_SUFFIX" : the output suffix added to the enhanced version of the input media,
- "SCORE_THRESHOLD" : the score threshold that decides if the audio quality of the input media is too low,

- "transcription_url" : the Azure cognitive services input URL for transcription, dependent on region.
- "tunneling_url" : The location of your Serverless HTTP trigger, or your HTTP tunnel (if you run locally) 

### Steps
- [Start by cloning this repo to your local machine.](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
#### Local with VS Code (Recommended for development)
- [Follow the guide here to get setup with VS Code, Azure functions, and Python.](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
- Once set up you can clone the project and open it in VS Code.
- [Create a HTTP tunnel with ngrok](https://ngrok.com/docs#http-local-https)
- - "ngrok" is a tunneling tool that allows you to port forward to local host.
- - In my case my local function was deployed on 7071, so I initalized ngrok to port forward on LocalHost:7071
- Adjust the "params.json" file with your HTTP ngrok Tunnel and the other appropriate params such as your blob name and API keys, then save the file. 
- Now you can press F5 to run the project.
- Once the code is running, navigate to http://localhost:"YOUR_SERVER"/api/MediaProcessingWorkflow?input_file="YOUR_INPUT_FILE" in your browser.
- - This will trigger the function to run locally, if all params are valid you can check your storage account for transcriptions or enhanced media.

#### Server with VS Code (Recommended for deployment)
- [Follow the guide here to get setup with VS Code, Azure functions, and Python.](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
- Once set up you can clone the project and open it in VS Code.
- Adjust the "params.json" file. 
- - In this case the tunneling URL will be https://"YOUR_FUNCTION_APP_NAME".azurewebsites.net/api/"YOUR_FUNCTION_NAME"
- - For example our tunneling URL is https://DolbyioMediaWorkflowTest.azurewebsites.net/api/MediaProcessingWorkflow
- Next deploy function app
- Once successfully deployed to the Azure Server you can test your function by navigating to: 
- - https://"YOUR_FUNCTION_APP_NAME".azurewebsites.net/api/"YOUR_FUNCTION_NAME"?input_file="YOUR_INPUT_FILE"

## References
- [Use Dolby.io to inspect, correct, and perfect your audio.](https://dolby.io/products/media-processing)
- [Azure Functions.](https://azure.microsoft.com/en-us/services/functions/)
- [Reach out for clarification @BradenRiggs1 on Twitter.](https://twitter.com/BradenRiggs1)
