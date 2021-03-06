"""Ecommerce API constants."""


class APIDictionaryKeys(object):
    """Dictionary keys used repeatedly in the ecommerce API."""
    BASKET_ID = u'id'
    CHECKOUT = u'checkout'
    ORDER = u'order'
    ORDER_NUMBER = u'number'
    ORDER_TOTAL = u'total'
    PAYMENT_DATA = u'payment_data'
    PAYMENT_FORM_DATA = u'payment_form_data'
    PAYMENT_PAGE_URL = u'payment_page_url'
    PAYMENT_PROCESSOR_NAME = u'payment_processor_name'
    PRODUCTS = u'products'
    SHIPPING_CHARGE = u'shipping_charge'
    SHIPPING_METHOD = u'shipping_method'
    SKU = u'sku'


class APIConstants(object):
    """Constants used throughout the ecommerce API."""
    FREE = 0
    KEYS = APIDictionaryKeys()
