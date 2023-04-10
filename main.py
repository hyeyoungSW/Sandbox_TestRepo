import requests
import openai
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
import sys

#Load the env file
project_folder = os.path.expanduser('./')
load_dotenv(os.path.join(project_folder,'.env'))

#ChatGPT apikey
openai.api_key = os.getenv('OPENAI_APIKEY')
 
#ServiceNow information
username = str(os.getenv("SERVICENOW_USERNAME"))
password = str(os.getenv("SERVICENOW_PASSWORD"))
snow_instance = str(os.getenv("SNOW_INSTANCE"))
api_url = "https://"+snow_instance+".service-now.com/"
incident_table_url = api_url + "api/now/table/incident"


def getIncidentTable():
    params = dict()
    incident_table = requests.get(incident_table_url, auth=(username, password), params=params).json()
    return incident_table


def getChatGPTCode(chatgpt_prompt):
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=chatgpt_prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
    )
    code = response.choices[0].text

    return code


def main():
    incident_number = input("Enter the incident number : ")

    code_version = incident_number + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = "LOG_" + code_version + '.txt'
    code_filename = code_version + '.py'

    log_folder = project_folder + 'Log/' + incident_number

    if(os.path.exists(project_folder + 'Log/') == False):
        os.mkdir(project_folder + 'Log/')

    if(os.path.exists(log_folder) == False):
        os.mkdir(log_folder)

    original_stdout = sys.stdout

    with open(log_folder+  '/' + log_filename, 'a') as f:
        sys.stdout = f

        try:
            #Get the ServiceNow incident table
            incident_table = getIncidentTable()
            chatgpt_prompt = ""
            print("----------------------------------------------")
            print(f"\nget the incident {incident_number} data...\n")

            #find the incident with incident number
            for inc in incident_table['result']:
                if inc['number'] == incident_number:
                    chatgpt_prompt = inc['description']
                    break

            print("----------------------------------------------")
            print("            [Incident description]            ")
            print("\n")
            print(chatgpt_prompt)
            print("\n\n")
            print("----------------------------------------------")


            #Request the code to ChatGPT
            created_code = getChatGPTCode(chatgpt_prompt)

            print("\nChatGPT is creating the code...\n")
            print("----------------------------------------------")
            print("                [Created Code]                \n")
            print(created_code)
            print("\n\n")
            print("----------------------------------------------")

            #Save the python code
            incident_folder = project_folder + 'CreatedCode/' + incident_number

            if(os.path.exists(project_folder + 'CreatedCode/') == False):
                os.mkdir(project_folder + 'CreatedCode/')

            if(os.path.exists(incident_folder) == False):
                os.mkdir(incident_folder)

            
            filepath = incident_folder + '/' + code_filename
            with open(filepath, 'a') as f:
                f.write(created_code)
                f.close()

            print("Code file has been created : " + code_filename)
            print("----------------------------------------------")
            print("Start to executing the created code" + code_filename)
            print("----------------------------------------------")


            #Execute the created python code
            exec(open(filepath).read())
            
            print("----------------------------------------------")

        except Exception as Argument:
            print(Argument)

        sys.stdout = original_stdout
        f.close()


    logfile = open(log_folder+  '/' + log_filename, 'r')
    print(logfile.read())
    f.close()

if __name__ == "__main__":
    main()