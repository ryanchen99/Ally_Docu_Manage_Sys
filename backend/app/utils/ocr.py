import cv2
import pytesseract
import PyPDF2
import numpy as np


def parse(file, file_obj):
    info = {'First_Name': None,
            'Last_Name': None,
            'License_Number': None,
            'SEX': None,
            'Date_of_Birth (MM/DD/YYYY)': None,
            'Hair': None,
            'Issue_Date (MM/DD/YYYY)': None,
            'Expiration_Date (MM/DD/YYYY)': None,
            'Restrictions': None,
            'Endorsements': None,
            'Class': None,
            'Address': None,
            'City': None,
            'State': None,
            'Zip': None,
            'Eyes': None,
            'Donor': None,
            'Height': None,
            'Weight': None,
            'Document Discriminator': None}
    ext = file.split('.')[-1].lower()
    if ext in ['jpg', 'jpeg', 'png']:
        file_bytes = np.asarray(bytearray(file_obj.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        text = pytesseract.image_to_string(blur)
    elif ext == 'pdf':
        pdf_reader = PyPDF2.PdfFileReader(file_obj)
        text = ""
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    else:
        raise ValueError("Unsupported file format")
        
    text = text.lower()
    lines = text.split('\n')
    
    for line in lines:
        if 'fn' in line:
            info['First_Name'] = line[line.index('fn') + 2:].strip()
        elif 'ln' in line:
            info['Last_Name'] = line[line.index('ln') + 2:].strip()
        elif 'dl' in line:
            info['License_Number'] = line[line.index('dl') + 2:].strip()
        elif 'sex' in line:
            info['SEX'] = line[line.index('sex') + 3:].strip()
        elif 'dob' in line:
            info['Date_of_Birth (MM/DD/YYYY)'] = line[line.index('dob') + 3:].strip()
        elif 'hair' in line:
            info['Hair'] = line[line.index('hair') + 3:].strip()
        elif 'iss' in line:
            info['Issue_Date (MM/DD/YYYY)'] = line[line.index('iss') + 3:].strip()
        elif 'exp' in line:
            info['Expiration_Date (MM/DD/YYYY)'] = line[line.index('exp') + 3:].strip()
        elif 'rstr' in line:
            info['Restrictions'] = line[line.index('rstr') + 4:].strip()
        elif 'end' in line:
            info['Endorsements'] = line[line.index('end') + 3:].strip()
        elif 'class' in line:
            info['Class'] = line[line.index('class') + 5:].strip()
        elif 'ca' in line:
            index = lines.index(line)
            address_lines = lines[index-2:index]
            info['Address'] = ' '.join(address_lines) + ' ' + line[line.index('ca'):].strip()
        elif 'eyes' in line:
            info['Eyes'] = line[line.index('eyes') + 4:].strip()
        elif 'donor' in line:
            info['Donor'] = 'yes'
        elif 'hgt' in line:
            info['Height'] = line[line.index('hgt') + 3:].strip()
        elif 'wgt' in line:
            info['Weight'] = line[line.index('wgt') + 3:].strip()
        elif 'dd' in line:
            info['Document Discriminator'] = line[line.index('dd') + 2:].strip()

    return info

def reformat_name(name):
    if name is None:
        return None
    formatted_name = name[0].upper() + name[1:].lower()
    return formatted_name

def reformat_sex(sex):
    if "f" in sex.lower():
        return "female"
    if "m" in sex.lower():
        return "male"
    else:
        return "Please Type to Specify"
    
def reformat_date(date):
    if date is None:
        return None
    import re
    date_pattern = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")
    date = re.search(date_pattern, date)
    if date:
        return date.group()
    else:
        return None


def parse_CA_DL(file, file_obj):
    info = parse(file, file_obj)
    info['First_Name'] = reformat_name(info['First_Name'])
    info['Last_Name'] = reformat_name(info['Last_Name'])
    info['SEX'] = reformat_sex(info['SEX'])
    info['Date_of_Birth (MM/DD/YYYY)'] = reformat_date(info['Date_of_Birth (MM/DD/YYYY)'])
    info['Issue_Date (MM/DD/YYYY)'] = reformat_date(info['Issue_Date (MM/DD/YYYY)'])
    info['Expiration_Date (MM/DD/YYYY)'] = reformat_date(info['Expiration_Date (MM/DD/YYYY)'])

    
    return info
# print(reformat_name('jOHN'))
# print(parse_CA_DL('CA_DL.png'))
# print(reformat_date('12/12/1999 sandf,f dv none'), type(reformat_date('12/12/1999 sandf,f dv none')))