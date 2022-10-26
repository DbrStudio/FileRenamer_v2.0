import multiprocessing
import os
import PySimpleGUI as sg
import pdfquery
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
import io
import shutil
import time
from multiprocessing import Pool


current_path = os.getcwd()
temp = os.path.join(current_path, "temp")
poppler_path = os.path.join(current_path, r"poppler-22.04.0\Library\bin")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def notImplemented():
    sg.popup(f'Feature not yet implemented!')


def initializeProgram():
    global current_path
    global temp

    current_path = os.getcwd()
    temp = os.path.join(current_path, "temp")

    if not os.path.isdir(temp):
        os.mkdir(temp)


# iterate directory
def list_PDF_files(art=None):
    # list to store files
    index = []
    if art == "temp":
        pfad = temp
    else:
        pfad = current_path
    for path in os.listdir(pfad):
        # check if current path is a file and a pdf
        if os.path.isfile(os.path.join(pfad, path)) and path.lower().endswith(".pdf"):
            index.append(path)
    return index


def ocrPDF(file_list=None):
    """
    if file_list is None:
        file_list = list_PDF_files()
    elif file_list == "temp":
        file_list = list_PDF_files(art="temp")
    """

    for i in file_list:
        start = time.time()
        # convert pdf into images
        images = convert_from_path(os.path.join(current_path, i), poppler_path=poppler_path)
        pdf_writer = PyPDF2.PdfFileWriter()
        #ocr on pages
        for image in images:
            print(f"processing file: {i}")
            page = pytesseract.image_to_pdf_or_hocr(image, lang='eng+deu', extension='pdf')
            pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
            pdf_writer.addPage(pdf.getPage(0))
        # copy ocr files to temp location
        with open(os.path.join(temp, "temp_"+ i), "wb") as f:
            pdf_writer.write(f)
        end = time.time()
        print(f"elapsed time:{end - start}")

def printPaths():
    print(f"current path: {current_path}")
    print(f"Temp Path: {temp}")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    files_list = ['CCF_000995.pdf', 'CCF_000996.pdf', 'CCF_000997.pdf', 'CCF_000998.pdf']

    total_start = time.time()
    with Pool() as pool:
        pool.imap_unordered(ocrPDF, files_list)
    total_end = time.time()

    print(f"finished after {total_end - total_start}")

