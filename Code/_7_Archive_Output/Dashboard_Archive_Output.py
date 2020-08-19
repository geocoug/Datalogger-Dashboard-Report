import datetime, os
import shutil

def archiveOutput():
    exe_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(exe_path)
    grandparent_dir = os.path.dirname(parent_dir)
    directory = os.path.dirname(grandparent_dir)

    today = datetime.datetime.now()
    m = today.strftime("%m")
    d = today.strftime("%d")
    y = today.strftime("%Y")


    if int(y) > int(2019):
        dir_num = int(m) + (int(12) * (int(y) - int(2019)))
    else:
        if int(m) < int(10):
            dir_num = '0{}'.format(int(m))
        else:
            dir_num = int(m)
        
    dir_month = today.strftime("%B")
    dir_year = y

    dir_name = '{} - {}{}'.format(dir_num, dir_month, dir_year)
    today = '{}-{}-{}'.format(y, m, d)

    img_folder = os.path.join(directory, '_Dashboard_Reports\Report_Output\Images\{}'.format(today))
    img_archive = os.path.join(directory, '_Dashboard_Reports\Report_Output\Images\{}'.format(dir_name))
    html_folder = os.path.join(directory, '_Dashboard_Reports\Report_Output\HTML\{}'.format(today))
    html_archive = os.path.join(directory, '_Dashboard_Reports\Report_Output\HTML\{}'.format(dir_name))
    pdf_dir = os.path.join(directory, '_Dashboard_Reports\Report_Output\PDF\{} Report For Dashboard.pdf'.format(today))
    pdf_archive = os.path.join(directory, '_Dashboard_Reports\Report_Output\PDF\{}'.format(dir_name))

    if os.path.exists(img_archive) == True:
        pass
    else:
        os.mkdir(img_archive)
    if os.path.exists(html_archive) == True:
        pass
    else:
        os.mkdir(html_archive)
    if os.path.exists(pdf_archive) == True:
        pass
    else:
        os.mkdir(pdf_archive)


    if os.path.exists(os.path.join(img_archive, today)) == True:
        pass
    else:
        shutil.move(img_folder, img_archive)
    if os.path.exists(os.path.join(html_archive, today)) == True:
        pass
    else:
        shutil.move(html_folder, html_archive)
    if os.path.exists(os.path.join(pdf_archive, '{} Report For Dashboard.pdf'.format(today))):
        pass
    else:
        shutil.move(pdf_dir, pdf_archive)


