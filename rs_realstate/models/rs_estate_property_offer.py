from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class RsPropertyOffer(models.Model):
    _name = 'rs.estate.property.offer'
    _inherit = 'estate.property.offer'
        
    property_id = fields.Many2one(
        string='Property',
        comodel_name='rs.estate.property',
        ondelete='restrict',
    )
    
    
