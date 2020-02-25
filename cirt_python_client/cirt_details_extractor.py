import csv
import requests
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from encode_user_credential import convertToUrlEncodedBase64

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import json
from zipfile import ZipFile

API_BASE_URL = "https://api.theexchange.fanniemae.com/v1/credit-insurance-risk-transfer/"
HEADER_FILE_NAME = '00CRT_Header_File.csv'
MANIFEST_FILE_NAME = 'manifest.txt'
HEADER_ROW_COPY=[]

def get_config_file():
    with open("cirt-config.json") as configFile:
        config = json.load(configFile)
    return config


config = get_config_file()
plain_text_credential = config['auth']
'Checking if the input credential is plain text'
if(":" in plain_text_credential):
    AUTH_TOKEN = convertToUrlEncodedBase64(plain_text_credential).decode("utf-8")
else:
    AUTH_TOKEN = plain_text_credential;


def get_headers():
    headers = {"Authorization": AUTH_TOKEN,
               "accept": "application/json",
               "Content-type": "application/json"}
    return headers


def send_request(http_method, url, data, headers):
    global response_body_status
    response_status = requests.request(method=http_method, url=url, data=data, headers=headers, verify=False)
    response_body_status = json.loads(response_status.text)
    return response_body_status


def get_header_row(extracted_zip_files, output_folder_name):
    global HEADER_ROW_COPY
    header_row = []
    for file in extracted_zip_files:
        if file == HEADER_FILE_NAME:
            header_file_name = f'{output_folder_name}/{file}'
            with open(header_file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='|')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Actual CSV coulmn names are {", ".join(row)}')
                        header_row = [
                            line.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("<",
                                                                                                             "").replace(
                                "=", "") for line
                            in row if line]
                        line_count += 1
                    else:
                        line_count += 1
                print(f'Processed {line_count} lines.')
                HEADER_ROW_COPY=header_row
    return header_row


class RowObject(object):

    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            if self.is_date(value):
                self.__dict__[key] = datetime.strptime(value, '%m%Y')
            elif self.is_integer(value):
                self.__dict__[key] = int(value)
            elif self.is_float(value):
                self.__dict__[key] = float(value)
            else:
                self.__dict__[key] = value

    def is_integer(self, value):
        try:
            val = int(value)
            return True;
        except ValueError:
            return False

    def is_date(self, value):
        try:
            # CIRT API returns date in MMYYYY format,
            # hence any string value which has length lesser than 5 will be considered as invalid date
            if len(value) < 6:
                return False
            datetime.strptime(value, '%m%Y')
            return True;
        except ValueError:
            return False;

    def is_float(self, value):
        try:
            val = float(value)
            return True;
        except ValueError:
            return False


def get_cirt_file_data(extracted_zip_files, output_folder_name):
    header_row = get_header_row(extracted_zip_files, output_folder_name)
    print(f'converted python object names are {header_row}')
    objects_data_list = []
    if header_row:
        for zip_file_name in extracted_zip_files:
            if zip_file_name != HEADER_FILE_NAME and zip_file_name != MANIFEST_FILE_NAME:
                data_file = f'{output_folder_name}/{zip_file_name}'
                print(f'extracting data from {data_file}  to python dict objects')
                with open(data_file) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter='|')
                    line_count = 0
                    for data_row in csv_reader:
                        row_object = RowObject(header_row, data_row)
                        line_count += 1
                        objects_data_list.append(row_object)
                    print(f'Processed {line_count} lines')
        print(f'data extracted to python dict objects')
    else:
        print(f'Header file does not exist can not map the data')
    return objects_data_list;

def get_header_properties():
    return  HEADER_ROW_COPY


def consume_and_store_response(s3_url_for_zip_file, output_file_name):
    files = ""
    response = requests.get(s3_url_for_zip_file, stream=True, verify=False)
    with open(output_file_name + ".zip", 'wb') as handle:
        for block in response.iter_content(32768):
            handle.write(block)
    # now unzip it
    with ZipFile(output_file_name + ".zip", 'r') as zipObj:
        files = zipObj.namelist()
        zipObj.extractall(output_file_name)
    return files
