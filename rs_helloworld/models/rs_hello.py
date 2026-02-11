
from odoo import models, fields, _

class RsHello(models.Model):
    _name = 'rs.hello'
    _description = 'Hello Message'

    #_rec_name = 'name'
    #_order = 'name ASC'

    name = fields.Char(
        string='Message',
        required=True,
        #default=lambda self: _('New'),
        #copy=False
    )

    
