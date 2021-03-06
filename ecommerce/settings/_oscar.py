"""Oscar-specific settings"""
from __future__ import absolute_import

from os.path import abspath, join, dirname

from django.core.urlresolvers import reverse_lazy
from oscar.defaults import *
from oscar import get_core_apps

from ecommerce.extensions.fulfillment.status import ORDER, LINE
from ecommerce.extensions.refund.status import REFUND, REFUND_LINE


# URL CONFIGURATION
OSCAR_HOMEPAGE = reverse_lazy('dashboard:index')
# END URL CONFIGURATION


# APP CONFIGURATION
OSCAR_APPS = [
    'ecommerce.extensions.api',
    'ecommerce.extensions.fulfillment',
    'ecommerce.extensions.refund',
] + get_core_apps([
    'ecommerce.extensions.analytics',
    'ecommerce.extensions.catalogue',
    'ecommerce.extensions.checkout',
    'ecommerce.extensions.order',
    'ecommerce.extensions.partner',
    'ecommerce.extensions.payment',
])
# END APP CONFIGURATION


# ORDER PROCESSING
# Prefix appended to every newly created order number.
ORDER_NUMBER_PREFIX = 'OSCR'

# The initial status for an order, or an order line.
OSCAR_INITIAL_ORDER_STATUS = ORDER.OPEN
OSCAR_INITIAL_LINE_STATUS = LINE.OPEN

# This dict defines the new order statuses than an order can move to
OSCAR_ORDER_STATUS_PIPELINE = {
    ORDER.OPEN: (ORDER.COMPLETE, ORDER.FULFILLMENT_ERROR),
    ORDER.FULFILLMENT_ERROR: (ORDER.COMPLETE,),
    ORDER.COMPLETE: ()
}

# This is a dict defining all the statuses a single line in an order may have.
OSCAR_LINE_STATUS_PIPELINE = {
    LINE.OPEN: (
        LINE.COMPLETE,
        LINE.FULFILLMENT_CONFIGURATION_ERROR,
        LINE.FULFILLMENT_NETWORK_ERROR,
        LINE.FULFILLMENT_TIMEOUT_ERROR,
        LINE.FULFILLMENT_SERVER_ERROR,
    ),
    LINE.FULFILLMENT_CONFIGURATION_ERROR: (LINE.COMPLETE,),
    LINE.FULFILLMENT_NETWORK_ERROR: (LINE.COMPLETE,),
    LINE.FULFILLMENT_TIMEOUT_ERROR: (LINE.COMPLETE,),
    LINE.FULFILLMENT_SERVER_ERROR: (LINE.COMPLETE,),
    LINE.COMPLETE: (),
}

# This dict defines the line statuses that will be set when an order's status is changed
OSCAR_ORDER_STATUS_CASCADE = {
    ORDER.OPEN: LINE.OPEN,
}

# Fulfillment Modules allows specific fulfillment modules to be evaluated in a specific order.
# Each fulfillment module supports handling a certain set of Product Types, and will evaluate the
# lines in the order to determine which it can fulfill.
FULFILLMENT_MODULES = [
    'ecommerce.extensions.fulfillment.modules.EnrollmentFulfillmentModule',
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

OSCAR_DEFAULT_CURRENCY = 'USD'
# END ORDER PROCESSING


# PAYMENT PROCESSING
PAYMENT_PROCESSORS = (
    'ecommerce.extensions.payment.processors.Cybersource',
    'ecommerce.extensions.payment.processors.Paypal',
)

PAYMENT_PROCESSOR_CONFIG = {
    'cybersource': {
        'profile_id': None,
        'access_key': None,
        'secret_key': None,
        'payment_page_url': None,
        'receipt_page_url': None,
        'cancel_page_url': None,
    },
    'paypal': {
        # 'mode' can be either 'sandbox' or 'live'
        'mode': None,
        'client_id': None,
        'client_secret': None,
        'receipt_url': None,
        'cancel_url': None,
    },
}
# END PAYMENT PROCESSING


# ANALYTICS
# Here Be Dragons: Use this feature flag to control whether Oscar should install its
# default analytics receivers. This is disabled by default. Some default receivers,
# such as the receiver responsible for tallying product orders, make row-locking
# queries which significantly degrade performance at scale.
INSTALL_DEFAULT_ANALYTICS_RECEIVERS = False
# END ANALYTICS


# REFUND PROCESSING
OSCAR_INITIAL_REFUND_STATUS = REFUND.OPEN
OSCAR_INITIAL_REFUND_LINE_STATUS = REFUND_LINE.OPEN

OSCAR_REFUND_STATUS_PIPELINE = {
    REFUND.OPEN: (REFUND.DENIED, REFUND.ERROR, REFUND.COMPLETE),
    REFUND.ERROR: (REFUND.COMPLETE, REFUND.ERROR),
    REFUND.DENIED: (),
    REFUND.COMPLETE: ()
}

OSCAR_REFUND_LINE_STATUS_PIPELINE = {
    REFUND_LINE.OPEN: (REFUND_LINE.DENIED, REFUND_LINE.PAYMENT_REFUND_ERROR, REFUND_LINE.PAYMENT_REFUNDED),
    REFUND_LINE.PAYMENT_REFUND_ERROR: (REFUND_LINE.PAYMENT_REFUNDED, REFUND_LINE.PAYMENT_REFUND_ERROR),
    REFUND_LINE.PAYMENT_REFUNDED: (REFUND_LINE.COMPLETE, REFUND_LINE.REVOCATION_ERROR),
    REFUND_LINE.REVOCATION_ERROR: (REFUND_LINE.COMPLETE, REFUND_LINE.REVOCATION_ERROR),
    REFUND_LINE.DENIED: (),
    REFUND_LINE.COMPLETE: ()
}
# END REFUND PROCESSING
