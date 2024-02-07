from nicegui import ui, native, app
import backend as b
import asyncio
from nicegui import ui, app, events
import time
import asyncio
import sys
from io import StringIO
import io
import os
from logging import getLogger, StreamHandler
from PyPDF2 import PdfReader

async def button_click(folder, log, system_role, user_role):
    global all_file_text
    all_file_text = await asyncio.to_thread(b.get_pdf_summary, folder, log, system_role, user_role)


def download_pdf(log):
    global all_file_text
    log.push("Downloading PDFs")
    print(all_file_text)
    for text in all_file_text:
         ui.download(text)


def clear():
    global all_file_text
    for text in all_file_text:
        os.remove(text)
    all_file_text = []
    log.clear()
    upload_func.refresh()

    
@ui.refreshable
def upload_func():
    global file_list
    file_list = []
    upload = ui.upload(
        label="Image",
        on_upload=file_list.append,
        auto_upload=True,
        multiple=True,
    )
    return upload

upload_func()
system_role = ui.textarea("System Role", value="Give the title and authors of the paper and Summarize the key points: ")
user_role = ui.textarea("User Role", value="You are a helpful research assistant.")

log = ui.log(20).classes("w-full").style("height: 400px; color: #ffffff; background-color: #000000; ")
ui.button("Summarise all pdfs", on_click=lambda: button_click(file_list, log, system_role, user_role))
ui.button("Download all pdfs", on_click=lambda: download_pdf(log))
ui.button("Clear All", on_click=lambda: clear())

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(reload = True, title="Article Summaries")
