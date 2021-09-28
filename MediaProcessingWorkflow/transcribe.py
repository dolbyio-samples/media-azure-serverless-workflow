#Functions for Azure Cognitive Services Speech to Text
#https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/#features

import requests
import logging
import json

with open("params.json", "r") as read_file:
    data = json.load(read_file)

def start(API_KEY,AUDIO_FILE,CONTAINER_OUTPUT):
    """
    Creates a transcription job on the Azure Cognitive Services server.
    Inputs:
       API_KEY: The Cognitive Service Transcription API key required for authenticating jobs.
       AUDIO_FILE: The SAS URL that points to the file for transcription.
       CONTAINER_OUTPUT: The SAS URL that directs the Azure server to where the transcription should go.
    Returns: 
       Post response.
    """

    #Submit a transcription job
    headers = {"Content-Type": "application/json","Ocp-Apim-Subscription-Key": API_KEY}
    body = {"contentUrls": [AUDIO_FILE],  
            "properties": {
                "diarizationEnabled": False,
                "wordLevelTimestampsEnabled": False,
                "punctuationMode": "DictatedAndAutomatic",
                "profanityFilterMode": "Masked",
                "destinationContainerUrl": CONTAINER_OUTPUT
            },
            "locale": "en-US",
            "displayName": "Transcribing media in a Dolby.io-Azure mediaflow"
    }

    response = requests.post(data["transcription_url"], headers=headers, json=body)
    response.raise_for_status()
    logging.info("Transcription Job Created Successfully, Check Input Container for Transcription...")
    return response
