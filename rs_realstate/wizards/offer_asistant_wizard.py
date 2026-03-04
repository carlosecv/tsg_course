# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OfferAsistantWizard(models.TransientModel):
    _name = 'offer.asistant.wizard'
    _description = 'Offer Assistant (Create Property + Offer)'

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    # =========================
    # Property fields
    # =========================
    address_id = fields.Many2one(
        comodel_name='res.partner',
        string='Property Address',
        ondelete='restrict',
        required=True,
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )

    currency_id = fields.Many2one(
        'res.currency',
        required=True,
        default=lambda self: self._default_currency_id(),
    )

    selling_price = fields.Monetary(
        string='Selling Price',
        currency_field="currency_id",
    )

    # =========================
    # Offer fields
    # =========================
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        ondelete='restrict',
        required=True,
    )

    price = fields.Monetary(
        string='Offer Price',
        currency_field='currency_id',
        required=True,
    )

    # Resultado (opcional para demo)
    property_id = fields.Many2one('estate.property', string='Created Property', readonly=True)
    offer_id = fields.Many2one('estate.property.offer', string='Created Offer', readonly=True)

    def action_create_property_and_offer(self):
        self.ensure_one()
        #import pdb;pdb.set_trace()
        if not self.address_id:
            raise UserError(_("Please select a Property Address."))
        if not self.customer_id:
            raise UserError(_("Please select a Customer for the Offer."))

        # 1) Crear la property
        prop_vals = {
            'partner_id': self.address_id.id,   # property address
            'user_id': self.user_id.id,
            'currency_id': self.currency_id.id,
            'selling_price': self.selling_price,
            'expected_price': self.selling_price or self.price,
        }
        prop = self.env['estate.property'].create(prop_vals)

        # 2) Crear la offer
        offer_vals = {
            'property_id': prop.id,
            'partner_id': self.customer_id.id,  # <-- aquí va el Customer de la oferta
            'currency_id': self.currency_id.id,
            'price': self.price,
        }
        offer = self.env['estate.property.offer'].create(offer_vals)

        self.write({'property_id': prop.id, 'offer_id': offer.id})

        return {
            'type': 'ir.actions.act_window',
            'name': _('Property'),
            'res_model': 'estate.property',
            'view_mode': 'form',
            'res_id': prop.id,
            'target': 'current',
        }

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}