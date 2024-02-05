import os
from openai import OpenAI
from PyPDF2 import PdfReader
import apikey
apikeyVal  = "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"
client = OpenAI(api_key=apikeyVal)
def get_pdf_summary(folder_path, log, system_role, user_role):
    # remove all " and ' from the folder path
    folder_path = folder_path.replace('"', '').replace("'", "")
    # Print number of files in the folder
    log.push(f"Number of files in the folder: {len([x for x in os.listdir(folder_path) if '.pdf' in x])}")
    for filename in os.listdir(folder_path):
        if ".pdf" in filename:
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                log.push(filename)
                pdf_summary_text = filename + "\n\n\n"
                # Open the PDF file
                pdf_file_path = file_path
                # Read the PDF file using PyPDF2
                pdf_file = open(pdf_file_path, 'rb')
                pdf_reader = PdfReader(pdf_file)
                page_text = pdf_reader.pages[0].extract_text().lower() + ' '
                for i in range(len(pdf_reader.pages)):
                    page_text += pdf_reader.pages[i].extract_text().lower()
                    page_text += ' '
                
                response = client.chat.completions.create(
                                model="gpt-4-turbo",
                                messages=[
                                    {"role": "system", "content": system_role.value},
                                    {"role": "user", "content": user_role.value + page_text},
                                        ],
                                            )
                page_summary = response.choices[0].message.content

                pdf_summary_text+=page_summary  + "\n\n"
                pdf_summary_file = pdf_file_path.replace(os.path.splitext(pdf_file_path)[1], "_summary.txt")
                with open(pdf_summary_file, "w+", encoding = 'utf-8') as file:
                    file.write(pdf_summary_text)

                pdf_file.close()
                log.push("Done")
                # log.push("Before Final Summary")
                # try:
                #     response = client.chat.completions.create(
                #                         model="gpt-4",
                #                         messages=[
                #                             {"role": "system", "content": "You are a helpful research assistant."},
                #                             {"role": "user", "content": f"Give the title and authors of the paper and Summarize the key points: {pdf_summary_text}"},
                #                                 ],
                #                                     )
                #     page_summary_final = filename + "\n\n\n"
                #     page_summary_final += response.choices[0].message.content
                #     pdf_summary_file_final = pdf_file_path.replace(os.path.splitext(pdf_file_path)[1], "_finalsummary.txt")
                #     with open(pdf_summary_file_final, "w+") as file:
                #         file.write(page_summary_final)
                #     log.push("file done")
                # except:
                #     log.push("Could not do final summary")
