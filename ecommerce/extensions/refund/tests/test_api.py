from decimal import Decimal
from unittest import TestCase

import ddt
from django.test import override_settings
from oscar.core.loading import get_model
from oscar.test.factories import create_order
from oscar.test.newfactories import UserFactory, BasketFactory

from ecommerce.extensions.fulfillment.status import ORDER
from ecommerce.extensions.refund.api import find_orders_associated_with_course, create_refunds
from ecommerce.extensions.refund.tests.factories import CourseFactory, RefundLineFactory


ProductAttribute = get_model("catalogue", "ProductAttribute")
ProductClass = get_model("catalogue", "ProductClass")
Refund = get_model('refund', 'Refund')

OSCAR_INITIAL_REFUND_STATUS = 'REFUND_OPEN'
OSCAR_INITIAL_REFUND_LINE_STATUS = 'REFUND_LINE_OPEN'


@ddt.ddt
class ApiTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

        self.course_id = u'edX/DemoX/Demo_Course'
        self.course = CourseFactory(self.course_id, u'edX Demo Course')
        self.honor_product = self.course.add_mode('honor', 0)
        self.verified_product = self.course.add_mode('verified', Decimal(10.00), id_verification_required=True)

    def _get_order(self):
        basket = BasketFactory(owner=self.user)
        basket.add_product(self.verified_product)
        order = create_order(basket=basket, user=self.user)
        order.status = ORDER.COMPLETE
        order.save()
        return order

    def test_find_orders_associated_with_course(self):
        """
        Ideal scenario: user has completed orders related to the course, and the verification close date has not passed.
        """
        order = self._get_order()
        self.assertTrue(self.user.orders.exists())

        actual = find_orders_associated_with_course(self.user, self.course_id)
        self.assertEqual(actual, [order])

    @ddt.data('', ' ', None)
    def test_find_orders_associated_with_course_invalid_course_id(self, course_id):
        """ ValueError should be raised if course_id is invalid. """
        self.assertRaises(ValueError, find_orders_associated_with_course, self.user, course_id)

    def test_find_orders_associated_with_course_no_orders(self):
        """ An empty list should be returned if the user has never placed an order. """
        self.assertFalse(self.user.orders.exists())

        actual = find_orders_associated_with_course(self.user, self.course_id)
        self.assertEqual(actual, [])

    @ddt.data(ORDER.OPEN, ORDER.FULFILLMENT_ERROR)
    def test_find_orders_associated_with_course_no_completed_orders(self, status):
        """ An empty list should be returned if the user has no completed orders. """
        order = self._get_order()
        order.status = status
        order.save()

        actual = find_orders_associated_with_course(self.user, self.course_id)
        self.assertEqual(actual, [])

    def test_create_refunds_verification_closed(self):
        """ No refunds should be created if the verification close date has passed. """
        self.fail()

    @override_settings(OSCAR_INITIAL_REFUND_STATUS=OSCAR_INITIAL_REFUND_STATUS,
                       OSCAR_INITIAL_REFUND_LINE_STATUS=OSCAR_INITIAL_REFUND_LINE_STATUS)
    def test_create_refunds(self):
        """ The method should create refunds for orders/lines that have not been refunded. """
        order = self._get_order()
        actual = create_refunds([order], self.course_id)
        refund = Refund.objects.get(order=order)
        self.assertEqual(actual, [refund])

        self.assertEqual(refund.order, order)
        self.assertEqual(refund.user, self.user)
        self.assertEqual(refund.status, OSCAR_INITIAL_REFUND_STATUS)
        self.assertEqual(refund.total_credit_excl_tax, order.total_excl_tax)
        self.assertEqual(refund.lines.count(), 1)

        refund_line = refund.lines.first()
        line = order.lines.first()
        self.assertEqual(refund_line.status, OSCAR_INITIAL_REFUND_LINE_STATUS)
        self.assertEqual(refund_line.order_line, line)
        self.assertEqual(refund_line.line_credit_excl_tax, line.line_price_excl_tax)
        self.assertEqual(refund_line.quantity, 1)

    def test_create_refunds_with_existing_refund(self):
        """ The method should NOT create refunds for lines that have already been refunded. """
        order = self._get_order()
        RefundLineFactory(order_line=order.lines.first())

        actual = create_refunds([order], self.course_id)
        self.assertEqual(actual, [])
