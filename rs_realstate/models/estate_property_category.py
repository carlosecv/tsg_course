from odoo import models,fields,_
from random import randint

class EstatePropertyCategory(models.Model):
    _name = 'estate.property.category'
    _description = 'Property Category'

    _rec_name = 'name'
    _order = 'name ASC'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(
        string='Category',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    color = fields.Integer(string='Color', default=_get_default_color, aggregator=False)
