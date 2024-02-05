from nicegui import ui, native, app
import backend as b
import asyncio
from nicegui import ui, app
import time
import asyncio
import sys
from io import StringIO
from logging import getLogger, StreamHandler

async def button_click(folder, log, system_role, user_role):
    await asyncio.to_thread(b.get_pdf_summary, folder, log, system_role, user_role)


folder = ui.input("Folder Path")
system_role = ui.textarea("System Role", value="Give the title and authors of the paper and Summarize the key points: ")
user_role = ui.textarea("User Role", value="You are a helpful research assistant.")

log = ui.log(20).classes("w-full").style("height: 400px; color: #ffffff; background-color: #000000; ")
ui.button("Summarise all pdfs", on_click=lambda: button_click(str(folder.value), log, system_role, user_role))

if __name__ == "__main__":
    ui.run(reload=False, port=native.find_open_port(), title="Signature Anomaly Detection Methods")
