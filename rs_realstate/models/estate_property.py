from odoo import models,fields,api,_

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'ModelName'

    _rec_name = 'name'
    _order = 'name ASC'


    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    
    @api.model_create_multi
    def create(self, vals_list):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """                
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code(
                    'estate.property') or _("New")
        # n next line of code
        # c continue without stop
        # l show lines of code
        # CTRL-D CTRL-INTERRUP stop all

        res = super().create(vals_list)
        return res
    

    name = fields.Char(
        string='Anounce Title',
        required=True,
        default=lambda self: _('New'),
        readonly=False,
        copy=False
    )
    
    property_type_id = fields.Many2one(
        string='Property Type',
        comodel_name='estate.property.type',
        ondelete='restrict',
    )
    
    postcode = fields.Char(string='Zip Code',related="partner_id.zip",readonly=False)
    
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
    
    brochure = fields.Binary(string='Brochure')

    brochure2 = fields.Binary(string='Brochure2',attachment=False)
    
    signature = fields.Binary(
        string="Firma"
    )

    image_1920 = fields.Image(
        string="Imagen",attachment=False,
        max_width=1920,
        max_height=1920
    )

    image_256 = fields.Image(
        string="Image 256",
        related="image_1920",
        max_width=256,
        max_height=256,
        store=True,
        attachment=False
    )

    image_128 = fields.Image(
        string="Image 128",
        related="image_1920",
        max_width=128,
        max_height=128,
        store=True,
        attachment=False,
    )


    partner_id = fields.Many2one(
        string='Property Address',
        comodel_name='res.partner',
        ondelete='restrict',
    )

    offer_count = fields.Integer(string='Offers',
        compute='_compute_offer_count' )
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    def action_open_estate_property_offers(self):        
        return {
            'name': _('Property Offers'),
            'type': 'ir.actions.act_window',
            'view_type': 'list',
            'view_mode': 'list,form',
            'res_model': 'estate.property.offer',
            'domain': [('id', 'in', self.ids)],
            'context': {
                        'search_default_property_id': self.id,
                        'default_property_id':self.id,
                        'default_price': 500000,
                        'default_currency_id': self.currency_id.id,
            },
        }
        
    
    