#Functions for Dolby.io Diagnose
#https://docs.dolby.io/media-processing/docs/quick-start-to-diagnosing-media

import requests
import logging

def start(API_KEY, INPUT_SAS, CALLBACK_DESTINATION):
    """
    Creates a diagnose job on the Dolby.io server.
    Inputs:
       API_KEY: The Dolby.io media API key required for authenticating jobs.
       INPUT_SAS: The SAS URL that points to the file for diagnosis.
       CALLBACK_DESTINATION: The HTTP location the callback should point to.
    Returns: 
       Post response
    """

    logging.info("Diagnosing Azure Stored Media")
    callback_destination = CALLBACK_DESTINATION + "?job=diagnose_success" + "&input_file=" + INPUT_SAS.split("?")[0].split("/")[-1]

    #Submit a diagnose job
    url = "https://api.dolby.com/media/diagnose"
    body = {"input" : INPUT_SAS, 
    'on_complete': {'url': callback_destination, "headers": ["x-job-id"]}}
    headers = {"x-api-key":API_KEY,"Content-Type": "application/json","Accept": "application/json", "x-job-id":"True"}

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    return response

def get_quality_score(API_KEY, JOB_ID):
    """
    Checks the average quality score of the diagnose job.
    Inputs:
       API_KEY: The Dolby.io media API key required for authenticating jobs.
       JOB_ID: The job ID that directs the server to your complete diagnose job.
    Returns: 
       Average audio quality for the input media.
    """

    #Check the outcome of the diagnose job
    url = "https://api.dolby.com/media/diagnose"
    headers = {"x-api-key": API_KEY,"Content-Type": "application/json","Accept": "application/json"}
    params = {"job_id": JOB_ID}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    res = response.json()
    logging.info("Outcome of diagnosis: " + str(res["result"]["audio"]["quality_score"]["average"]))

    return res["result"]["audio"]["quality_score"]["average"]
