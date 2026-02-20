from odoo import models,fields,_

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'ModelName'

    _rec_name = 'name'
    _order = 'name ASC'


    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    name = fields.Char(
        string='Anounce Title',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )
    
    property_type_id = fields.Many2one(
        string='Property Type',
        comodel_name='estate.property.type',
        ondelete='restrict',
    )
    
    postcode = fields.Char(string='Zip Code')
    
    currency_id = fields.Many2one('res.currency',required=True,default=lambda self: self._default_currency_id())

    expected_price = fields.Monetary(string='Expected Price',currency_field="currency_id")
    
    selling_price = fields.Monetary(string='Selling Price',currency_field="currency_id")

    bedrooms = fields.Integer(string='Bedrooms')    
    living_area = fields.Integer(string='Living Area [m2]')    
    garage = fields.Boolean(string='Garage')    
    garden = fields.Boolean(string='Garden')    

    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_id',
    )
    
    start_date = fields.Date(string='Start Date')
    
    state = fields.Selection(
        string='State',
        selection=[('draft', 'New'), 
                    ('receive', 'Offert Received'),  
                    ('accepted', 'Offer Accept'),  
                    ('sold', 'Sold')],
        default='draft',
        readonly=False,
    )
    
    categ_ids = fields.Many2many(
        string='Category',
        comodel_name='estate.property.category'
    )
    
    active = fields.Boolean(string='Active',default=True)
    
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",        
        readonly=False, index=True,
        tracking=2,)
    