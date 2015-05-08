"""
Prototype of PayPal report downloads.

https://developer.paypal.com/docs/classic/express-checkout/ht_searchRetrieveTransactionData-curl-etc/

NOTE: This filename ends with an underscore (_) to avoid a conflict the with the third-party API
client module.

USERNAME=reporter PASSWORD=secret SIGNATURE=xxx python reporting/paypal_.py
"""
import os

from paypal import PayPalInterface


client = PayPalInterface(
    API_USERNAME=os.environ['USERNAME'],
    API_PASSWORD=os.environ['PASSWORD'],
    API_SIGNATURE=os.environ['SIGNATURE']
)

transactions = client.transaction_search(STARTDATE='2015-05-01T00:00:00Z')

# FIXME XCOM-302 should (hopefully) add an invoice_number field to these transactions so that we know
# to which orders they correspond.
for index, transaction in transactions.iteritems():
    print transaction
