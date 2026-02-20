from odoo import models,fields,_


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    _rec_name = 'partner_id'
    _order = 'partner_id ASC'

    
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    property_id = fields.Many2one(
        string='Property',
        comodel_name='estate.property',
        ondelete='restrict',
    )
    

    partner_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner',
        ondelete='restrict',
    )
    currency_id = fields.Many2one('res.currency',required=True,default=lambda self: self._default_currency_id())
    price = fields.Monetary(string='Offert Price',currency_field='currency_id')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'New'), ('accepted', 'Acepted'),  ('reject', 'Rejected'),  ('cancel', 'Cancel')],
        default='draft',
        readonly=True,
    )
    validity_days = fields.Integer(string='Validity Days')
    deadline  = fields.Date(string='Deadline')
    
    sequence = fields.Integer(string='Sequence')
    
    
