"""
Prototype of CyberSource report downloads.

Based on documentation located at
http://apps.cybersource.com/library/documentation/dev_guides/Reporting_Developers_Guide/reporting_dg.pdf.

Requires CyberSource credentials from environment variables:
    $ USERNAME=reporter PASSWORD=password python reporting/cybersource.py
"""
import csv
import StringIO
import os

import requests


AUTH = (os.environ['USERNAME'], os.environ['PASSWORD'])

# Set to ebc.cybersource.com/ebc to retrieve production data. This requires production credentials.
HOST = 'ebctest.cybersource.com/ebctest'

MERCHANT_ID = 'edx_org'
REPORT_NAME = 'PaymentBatchDetailReport'
REPORT_FORMAT = 'csv'

# Create the URL
url = 'https://{host}/DownloadReport/{date}/{merchant_id}/{report_name}.{report_format}'.format(
    host=HOST,
    date='2015/05/06',
    merchant_id=MERCHANT_ID,
    report_name=REPORT_NAME,
    report_format=REPORT_FORMAT
)

# Download the report
response = requests.get(url, auth=AUTH)

# Read the data into a buffer
data = StringIO.StringIO(response.content)

# Skip first row as it simply describes the report that was downloaded.
data.readline()

# Parse the remaining data
reader = csv.reader(data, delimiter=',')
for row in reader:
    print '\t'.join(row)
