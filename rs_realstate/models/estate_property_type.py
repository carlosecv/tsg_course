from odoo import models,fields,_

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Property Type',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    active = fields.Boolean(string='Available', default=True)    

    _sql_constraints = [
        ('estate_property_type_name_uniq', 'unique(name)', _('Attribute Name must be unique!'))        
        ]