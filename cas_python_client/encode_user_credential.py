from urllib.parse import quote
from base64 import b64encode

''' Given plain text userName and password with colon separated string,
 it generates the Base64 URL encoded value
 For example test@email.com:mypassword
 The output will be URL encoded Base64 value 'dGVzdDEyMyU0MGVtYWlsLmNvbSUzQW15cGFzc3dvcmQ='
'''
def convertToUrlEncodedBase64(plainTextUserIdPass):
    print("Plain Text: ", plainTextUserIdPass)

    # URL Encoding the plain text
    urlEncodedHeaders = quote(plainTextUserIdPass)
    print("URL encoding value " + urlEncodedHeaders)

    # encoding the header with base64
    bytesHeaderToBePassed = bytes(urlEncodedHeaders, encoding='utf-8')
    encodedHeaders = b64encode(bytesHeaderToBePassed)
    return encodedHeaders