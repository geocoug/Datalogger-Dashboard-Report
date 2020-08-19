#!/usr/bin/python

#https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images

from fpdf import FPDF
import shutil, datetime, sys, os
from openpyxl import load_workbook
from PyPDF2 import PdfFileWriter, PdfFileReader
from shutil import copyfile


exe_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(exe_path)
grandparent_dir = os.path.dirname(parent_dir)
directory = os.path.dirname(grandparent_dir)


def main():
    create_pdf()

    
def create_pdf():
    today = datetime.datetime.now()
    m = today.strftime("%m")
    d = today.strftime("%d")
    y = today.strftime("%Y")
    today = '{}-{}-{}'.format(y, m, d)

    img_folder = os.path.join(directory, '_Dashboard_Reports\Report_Output\Images\{}'.format(today))
    img_names = os.listdir(img_folder)

    if len(img_names) == 0:
        print 'No images were downloaded. Please restart the program.'
        return

    img_names_sorted = []

    if len(img_names) == 5:
        img_names_sorted.extend(('{} System Daily Summary.png'.format(today),
                                 '{} SVE Flow Daily Summary.png'.format(today),
                                 '{} CombTemp LEL Cycle.png'.format(today),
                                 '{} Flow.png'.format(today),
                                 '{} Thermocouples.png'.format(today)))
                                 
    elif len(img_names) == 4:
        img_names_sorted.extend(('{} System Daily Summary.png'.format(today),
                                 '{} SVE Flow Daily Summary.png'.format(today),
                                 '{} CombTemp LEL Cycle.png'.format(today),
                                 '{} Flow.png'.format(today),))
    else:
        print 'Not all images were downloaded. Restart the program.'
        exit()
            

    fpdf = FPDF()
    
    for img in img_names_sorted:
        image = os.path.join(img_folder, img)
        if img == '{} System Daily Summary.png'.format(today):
            fpdf.add_page(orientation = 'L')
            fpdf.image(image, x=None, y=None, w=270, h=210, type='PNG', link='')

        elif img == '{} SVE Flow Daily Summary.png'.format(today):
            fpdf.add_page(orientation = 'L')
            fpdf.image(image, x=None, y=None, w=270, h=210, type='PNG', link='')

        elif img == '{} CombTemp LEL Cycle.png'.format(today):
            fpdf.add_page(orientation = 'L')
            fpdf.image(image, x=None, y=None, w=300, h=200, type='PNG', link='')

        elif img == '{} Flow.png'.format(today):
            fpdf.add_page(orientation = 'L')
            fpdf.image(image, x=None, y=None, w=300, h=200, type='PNG', link='')
            
        elif img == '{} Thermocouples.png'.format(today):
            fpdf.add_page(orientation = 'L')
            #fpdf.format('A3')
            fpdf.image(image, x=None, y=None, w=290, h=200, type='PNG', link='')#285x200
        else:
            pass

    pdf_temp = os.path.join(directory, r'_Dashboard_Reports\Report_Output\PDF\{} Temp.pdf'.format(today))
    fpdf.output(pdf_temp)

    if len(img_names) == 5:
        pages_to_keep = [1, 3, 5, 7, 9]
    elif len(img_names) == 4:
        pages_to_keep = [1, 3, 5, 7]
    else:
        print 'Not enough charts/tables to create PDF. Restart program.'
        exit()

    infile = PdfFileReader(pdf_temp, 'rb')
    output = PdfFileWriter()

    for i in pages_to_keep:
        p = infile.getPage(i)
        output.addPage(p)

    pdf_dir = os.path.join(directory, r'_Dashboard_Reports\Report_Output\PDF\{} Report For Dashboard.pdf'.format(today))

    with open(pdf_dir, 'wb') as f:
        output.write(f)

    os.remove(pdf_temp)
    
    print ''
    print 'Complete.'
    print '\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Output files located here: {}\_Dashboard_Reports\Report_Output'.format(directory)
    print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    print '\n'
    
    send_dashboard(pdf_dir, today)

def send_dashboard(pdf_dir, today):

    while True:
        print 'Review charts before continuing.\n'
        print 'Email Dashboard Report?'
        print '  (Y) Send Dashboard'
        print '  (N) Return to main menu\n'
        user_input = raw_input('Selection: ')
        print ''
        if user_input.upper() == 'Y':
            import win32com.client as win32
            print 'Sending PDF'
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = ''

            mail.Subject = 'Dashboard'
            mail.Body = 'Attached is the latest dashboard report.'

            attachment = pdf_dir
            mail.Attachments.Add(attachment)
##            attachment = html_zip_dir
##            mail.Attachments.Add(attachment)

            mail.Send()
            break
        
        elif user_input.upper() == 'N':
            return
        else:
            continue



        
if __name__ == '__main__':
    main()
