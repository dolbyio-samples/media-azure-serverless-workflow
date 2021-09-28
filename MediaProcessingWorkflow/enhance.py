#Functions for Dolby.io Enhance
#https://docs.dolby.io/media-processing/docs/quick-start-to-enhancing-media

import requests
import logging

def start(API_KEY, INPUT_SAS, OUTPUT_SAS, CALLBACK_DESTINATION):
    """
    Creates a enhance job on the Dolby.io server.
    Inputs:
       API_KEY: The Dolby.io media API key required for authenticating jobs.
       INPUT_SAS: The SAS URL that points to the file for enhancement.
       OUTPUT_SAS: The SAS URL that directs the Dolby.io server to where the enhanced file should go.
       CALLBACK_DESTINATION: The HTTP location the callback should point to.
    Returns: 
       Post response.
    """
    logging.info("Enhancing Input Media")
    callback_destination = CALLBACK_DESTINATION + "?job=enhance_success" + "&input_file=" + INPUT_SAS.split("?")[0].split("/")[-1]
    logging.info(callback_destination)

    #Submit an enhance job
    url = "https://api.dolby.com/media/enhance"
    body = {"input" : INPUT_SAS,"output": OUTPUT_SAS, 'on_complete': {'url': callback_destination}}
    headers = {"x-api-key":API_KEY, "Content-Type": "application/json", "Accept": "application/json"}

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    return response
