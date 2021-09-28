#Initialization function for the Azure Serverless Conf Dolby.io Demo
#https://docs.dolby.io/media-processing/docs
#By Braden Riggs
#https://twitter.com/BradenRiggs1

import logging
import json
import azure.functions as func
from . import diagnose
from . import enhance
from . import transcribe
from . import create_sas

#Reads the params file
#For a guide to the params file see the README.md
with open("params.json", "r") as read_file:
    data = json.load(read_file)

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main, responds to HttpRequests.
    Inputs:
       req: Posted HttpRequest that makes function serverless.
    """

    job_stat = req.params.get('job')
    azure_blob_input = req.params.get('input_file')


    if job_stat == None:
        #Starts by diagnosing the audio of the input file
        logging.info("STARTING MEDIA WORKFLOW FOR: " + azure_blob_input)

        input_sas, output_sas = create_sas.create_azure_blob_sas(data["AZURE_ACC_NAME"],data["AZURE_CONTAINER"],azure_blob_input,data["azure_api_key"],data["AZURE_BLOB_OUTPUT_SUFFIX"])
        diagnose.start(data["dolbyio_api_key"], input_sas, data["tunneling_url"])

    elif job_stat == "diagnose_success":
        #Upon success of diagnosis the file, pipeline then checks for the quality of the audio
        job_id = req.headers['x-job-id']

        if diagnose.get_quality_score(data["dolbyio_api_key"], job_id) > data["SCORE_THRESHOLD"]:
            #If the file has high quality audio we can skip enhancing the audio
            logging.info("QUALITY AUDIO, NO NEED FOR ENHANCING ON FILE: " + azure_blob_input)
            input_sas, output_sas = create_sas.create_azure_blob_sas(data["AZURE_ACC_NAME"],data["AZURE_CONTAINER"],azure_blob_input,data["azure_api_key"],data["AZURE_BLOB_OUTPUT_SUFFIX"])
            transcribe.start(data["cog_api_key"], input_sas)
        else:
            #If the file has low quality audio we instead enhance the file
            logging.info("LOW QUALITY AUDIO, ENHANCING FILE: " + azure_blob_input)
            input_sas, output_sas = create_sas.create_azure_blob_sas(data["AZURE_ACC_NAME"],data["AZURE_CONTAINER"],azure_blob_input,data["azure_api_key"],data["AZURE_BLOB_OUTPUT_SUFFIX"])
            enhance.start(data["dolbyio_api_key"], input_sas, output_sas, data["tunneling_url"])

    else:
        #Procceed to transcription for either original or enhanced media
        logging.info("STARTING TRANSCRIPTION OF: " + azure_blob_input)
        input_sas, output_sas = create_sas.create_azure_blob_sas(data["AZURE_ACC_NAME"],data["AZURE_CONTAINER"],azure_blob_input,data["azure_api_key"],"_output.json")
        container_sas = create_sas.create_container_sas(data["AZURE_ACC_NAME"],data["AZURE_CONTAINER"],data["azure_api_key"])
        transcribe.start(data["cog_api_key"], input_sas, container_sas)

    return func.HttpResponse("", status_code=200)
    
    
