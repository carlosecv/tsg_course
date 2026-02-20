from odoo import models,fields,_

class EstatePropertyCategory(models.Model):
    _name = 'estate.property.category'
    _description = 'Property Category'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Category',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )