from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class RsProperty(models.Model):
    _name = 'rs.estate.property'
    _inherit = 'estate.property'


    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='rs.estate.property.offer',
        inverse_name='property_id',
    )


    def action_open_estate_property_offers(self):
        context = self.env.context
        if context.get('my_flag'):
            return {
                'name': _('RS Property Offers'),
                'type': 'ir.actions.act_window',
                'view_type': 'list',
                'view_mode': 'list,form',
                'res_model': 'rs.estate.property.offer',
                'domain': [('id', 'in', self.ids)],
                'context': {
                            'search_default_property_id': self.id,
                            'default_property_id':self.id,
                            'default_price': 500000,
                            'default_currency_id': self.currency_id.id,
                },
            }
        else:
            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'This is a Message Test',
                'message': 'My Flag is False se ejecutó correctamente.',
                'type': 'success',
                'sticky': False,
            }
        }


