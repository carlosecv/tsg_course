
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class OfferAsistantWizard(models.TransientModel):
    _name = 'offer.asistant.wizard'
    _description = 'Offer Asistant'

    # This model creates a property and offer agile

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    address_id = fields.Many2one(
        string='Address',
        comodel_name='res.partner',
        ondelete='restrict',
    )

    currency_id = fields.Many2one('res.currency',required=True,default=lambda self: self._default_currency_id())
    price = fields.Monetary(string='Offert Price',currency_field='currency_id')
    selling_price = fields.Monetary(string='Selling Price',currency_field="currency_id")

    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",        
        readonly=False, index=True,
        tracking=2)



    
