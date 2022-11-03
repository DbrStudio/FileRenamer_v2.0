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

# import main

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
    # convert pdf into images
    images = convert_from_path(os.path.join(current_path, file_list), poppler_path=poppler_path)
    pdf_writer = PyPDF2.PdfFileWriter()

    # perform ocr on pages
    for image in images:
        page = pytesseract.image_to_pdf_or_hocr(image, lang='eng+deu', extension='pdf')
        pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
        pdf_writer.addPage(pdf.getPage(0))
    # copy ocr files to temp location
    with open(os.path.join(temp, "temp_" + file_list), "wb") as f:
        pdf_writer.write(f)


def ocrPooled(files_list):
    with Pool() as pool:
        pool.map(ocrPDF, files_list)
        # list(pool.imap_unordered(ocrPDF, files_list))


def renameFiles(files):
    new_path = os.path.join(temp, files)
    pdf = pdfquery.PDFQuery(new_path)
    pdf.load()
    name = pdf.pq('LTTextLineHorizontal:overlaps_bbox("138, 1800, 420, 1940")').text()
    name = str(name.split()[0] + ".pdf")
    pdf.file.close()
    try:
        shutil.copyfile(new_path, current_path + '\\renamed\\' + name)
    except FileNotFoundError:
        os.mkdir(current_path + "\\renamed\\")
        shutil.copyfile(new_path, current_path + '\\renamed\\' + name)


def printPaths():
    print(f"current path: {current_path}")
    print(f"Temp Path: {temp}")


def rmfiles():
    for file in os.listdir(temp):
        file_path = os.path.join(temp, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def renamePooled(file_list):
    with Pool() as pool:
        list(pool.imap_unordered(renameFiles, file_list))


"""
if __name__ == '__main__':

    

    
"""
