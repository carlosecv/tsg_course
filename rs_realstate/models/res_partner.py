from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    is_property = fields.Boolean()

    
    
