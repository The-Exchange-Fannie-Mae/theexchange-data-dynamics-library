import json
import time
from datetime import datetime
import sys
from cirt_details_extractor import get_cirt_file_data, consume_and_store_response, get_headers, API_BASE_URL, send_request,get_header_properties

LOAN_HEADER_FILE_NAME = '00CRT_Header_File.csv'
REQUEST_COMPLETED = 'completed'


def get_loan_query_request_payload(spec_file_name):
    payload = ''
    payload = ''
    with open(spec_file_name) as json_data:
        payload_dict = json.load(json_data)
        payload = json.dumps(payload_dict)
    return payload;


def get_loan_request_zip_url(spec_file_name):
    headers = get_headers()
    loan_request_url = f'{API_BASE_URL}loan-level-query'
    response_body = send_request("POST", loan_request_url, get_loan_query_request_payload(spec_file_name), headers)
    request_id = response_body.get('request-id')
    s3_url_for_zip_file = ''
    if request_id is not None:
        print(f'Request {request_id}  sent for loan request')
        sys.stdout.flush()
        cust_download_request_status_url = f'{API_BASE_URL}custom-download/status/{request_id}'
        cust_download_request_status_response = send_request("GET", cust_download_request_status_url, None, headers)
        cur_state = cust_download_request_status_response.get('currentState')
        # setting the uri if reuest status is completed for first time
        s3_url_for_zip_file = cust_download_request_status_response.get('s3Uri')
        print(f'{request_id} started at {datetime.now()}')
        while cur_state != REQUEST_COMPLETED:
            time.sleep(10)
            response_status_loop = send_request("GET", cust_download_request_status_url, None, headers)
            cur_state = response_status_loop.get('currentState')
            s3_url_for_zip_file = response_status_loop.get('s3Uri')
            print(f'request {request_id} current status is {cur_state}')
            sys.stdout.flush()
        print(f'{request_id} completed  at {datetime.now()}')
        sys.stdout.flush()
    else:
        print('error received from loan query endpoint')
        sys.stdout.flush()
    return s3_url_for_zip_file


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage:  client specification-file-name output-file-name")
        exit(-1)
    spec_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    print("executing query from file " + spec_file_name + " and sending output to " + output_file_name)
    sys.stdout.flush()
    s3_url_for_zip_file = get_loan_request_zip_url(spec_file_name)
    time.sleep(10)
    extracted_zip_files = consume_and_store_response(s3_url_for_zip_file, output_file_name)
    loan_objects_data_list = get_cirt_file_data(extracted_zip_files,output_file_name)
    print(f'length of python object list for cirt loan {len(loan_objects_data_list)}')
    header_row = get_header_properties()
    print(f'printing first row value for python objects')
    for header in header_row:
        print(f' header property {header} value  {loan_objects_data_list[0].__dict__.get(header)}')
    print('Printed first row values')
