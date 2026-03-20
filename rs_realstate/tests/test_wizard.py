# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class TestOfferAssistantWizard(TransactionCase):

    def setUp(self):
        super().setUp()
        self.address = self.env['res.partner'].create({
            'name': 'Address Test',
        })
        self.customer = self.env['res.partner'].create({
            'name': 'Customer Test',
        })

    def test_wizard_backend_create_property_and_offer(self):
        wizard = self.env['offer.asistant.wizard'].create({
            'address_id': self.address.id,
            'customer_id': self.customer.id,
            'price': 120000,
            'selling_price': 150000,
        })

        action = wizard.action_create_property_and_offer()

        self.assertTrue(wizard.property_id)
        self.assertTrue(wizard.offer_id)
        self.assertEqual(wizard.property_id.partner_id, self.address)
        self.assertEqual(wizard.offer_id.partner_id, self.customer)
        self.assertEqual(wizard.offer_id.price, 120000)
        self.assertEqual(action['res_model'], 'estate.property')

    def test_wizard_form_flow(self):
        with Form(self.env['offer.asistant.wizard']) as form:
            #form.address_id = self.address
            form.customer_id = self.customer
            form.selling_price = 150000
            form.price = 120000

        wizard = form.save()
        action = wizard.action_create_property_and_offer()

        self.assertTrue(wizard.property_id)
        self.assertTrue(wizard.offer_id)
        self.assertEqual(wizard.property_id.partner_id, self.address)
        self.assertEqual(wizard.offer_id.partner_id, self.customer)
        self.assertEqual(wizard.offer_id.price, 120000)
        self.assertEqual(action['res_id'], wizard.property_id.id)