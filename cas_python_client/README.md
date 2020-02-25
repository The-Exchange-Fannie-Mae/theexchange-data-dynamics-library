
# cas-python3-clients
cas api python3 clients, including code samples to  submit requests, and process responses both small and large.


### Installation Instructions:

	Step1: Create a directory into which you can clone this repo; that directory's name will become the value for
	the EXCHANGE_CLIENT_CAS_HOME environment variable.  This document will use $HOME/cas_python_client as the example name of 
	this directory.
	
	Step2:  Set the EXCHANGE_CLIENT_HOME environment variable to $HOME/cas_python_client and cd into that directory:
		bash--> export EXCHANGE_CLIENT_CAS_HOME=$HOME/cas_python_client
		bash--> cd $EXCHANGE_CLIENT_CAS_HOME

	Step3: Use git clone to obtain the client code and config files 
	
	step-4: Install dependencies required for running python_client_cas_loan-level-query.py and python_client_cas_custom_download.py
	Step-5: Add your auth key or plain text user and password if you are a Data Dynamic user in cas-config.json file
	     Ex: test@email.com:mypassword
	Step-6: Run a smoke test by passing the command line arguments; if successful it will get S3 location of CAS zip file and extract it and add the data in python dict objects:
		bash--> python python_client_cas_custom_download.py <input_request_file_name> <output_response_folder>
		Ex: python python_client_cas_custom_download.py cas-custom-download-one-deal.json custom_download
		bash--> python python_client_cas_loan-level-query.py <input_request_file_name> <output_response_folder>
		EX: python python_client_cas_loan-level-query.py mandoline-one-month-ltv-and-dti-spec-include-issaunce-and-remittance.json  loan_search_include_issuance_and_remittance


| Base Modules | Description |
| --- | --- |
| python python_client_cas_custom_download.py | Sample code for post request to custom download request and wait for the request to get completed and get the S3 ZIP URL for completed requests|
| python_client_cas_loan-level-query.py | Sample code for post request to loan level request and wait for the request to get completed and get the S3 ZIP URL for completed requests |


| Sample Request Files | Description |
| --- | --- |
| cas-custom-download-one-deal.json| sample json request file for invoking custom download endpoint, you can change the request details according to your need and the client program|
| mandoline-one-month-ltv-and-dti-spec.json | sample json request file for invoking loan request endpoint, you can change the request details according to your need and the client program. |
| 
Note: Since Python client making multiple api calls and extracting the data to python objects, client will take time to complete the programme and once the programme is completed you can see the print statement with Python dict objects list.
   EX: length of python object list for cas loan 62468