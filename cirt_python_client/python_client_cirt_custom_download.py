import json
import os
import time
import datetime
import sys
from cirt_details_extractor import get_cirt_file_data, consume_and_store_response, get_headers, API_BASE_URL, send_request, get_header_properties

REQUEST_COMPLETED = 'completed'
os.environ['NO_PROXY'] = 'localhost'


def get_cust_download_request_payload(spec_file_name):
    payload = ''
    with open(spec_file_name) as json_data:
        payload_dict = json.load(json_data)
        payload = json.dumps(payload_dict)
    return payload;


def get_cust_download_zip_url(spec_file_name):
    headers = get_headers()
    cust_api_download_url = f'{API_BASE_URL}custom-download'
    response_body = send_request("POST", cust_api_download_url, get_cust_download_request_payload(spec_file_name), headers)
    request_id = response_body.get('request-id')
    s3_url_for_zip_file = ''
    if request_id is not None:
        print(f'Request {request_id}  sent for custom download')
        cust_download_request_status_url = f'{API_BASE_URL}custom-download/status/{request_id}'
        cust_download_request_status_response = send_request("GET", cust_download_request_status_url, None, headers)

        cur_state = cust_download_request_status_response.get('currentState')
        print(f'{request_id} started at {datetime.datetime.now()}')
        # setting the uri if reuest status is completed for first time
        s3_url_for_zip_file = cust_download_request_status_response.get('s3Uri')
        while cur_state != REQUEST_COMPLETED:
            print(f'checking request {request_id} status')
            time.sleep(30)
            response_status_loop = send_request("GET", cust_download_request_status_url, None, headers)
            cur_state = response_status_loop.get('currentState')
            s3_url_for_zip_file = response_status_loop.get('s3Uri')
            print(f'request {request_id} current status is {cur_state}')
        print(f'{request_id} completed  at {datetime.datetime.now()}')
    else:
        print("error received from custom download endpoint")

    return s3_url_for_zip_file


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage:  client specification-file-name output-file-name")
        exit(-1)
    spec_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    print("executing query from file " + spec_file_name + " and sending output to " + output_file_name)
    sys.stdout.flush()
    s3_url_for_zip_file = get_cust_download_zip_url(spec_file_name)
    print(f's3 url to download cirt file ..... {s3_url_for_zip_file}')
    extracted_zip_files = consume_and_store_response(s3_url_for_zip_file, output_file_name)
    custom_download_objects_data_list = get_cirt_file_data(extracted_zip_files,output_file_name)
    print(f'length of python object list for cirt download {len(custom_download_objects_data_list)}')
    header_row=get_header_properties()
    print(f'printing first row value for python objects')
    for header in header_row:
      print(f' header property {header} value  {custom_download_objects_data_list[0].__dict__.get(header)}')
    print('Printed first row values')
