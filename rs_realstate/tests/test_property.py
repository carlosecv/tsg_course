from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Cliente Prueba',
        })
        cls.property = cls.env['estate.property'].create({
            'name': 'Casa Test',
            'expected_price': 1500000,
            'partner_id': cls.partner.id,
        })

    def test_cannot_sell_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_total_area_compute(self):
        self.property.write({
            'living_area': 120,
            'garden': True,
            'garden_area': 30,
        })
        self.assertEqual(self.property.total_area, 150)