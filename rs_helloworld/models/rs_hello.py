
from odoo import models, fields, _

NOTE_AGE_FIELDS = """Age of the Publisher, this must be filled in a range
of 20 to 65 years only"""

class RsHello(models.Model):
    _name = 'rs.hello'
    _description = 'Hello Message'

    #_rec_name = 'name'
    #_order = 'name ASC'

    name = fields.Char(
        string='Message',
        required=True,
        default=lambda self: _('New'),
        copy=False,
        size=100,
        trim=True,
        translate=True,
        help="""This field is for the Message to publish"""
    )

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    


    
    age = fields.Integer(copy=False, help=NOTE_AGE_FIELDS,
    groups="rs_helloworld.rs_hello_admin")
    
    amount = fields.Float(copy=False, 
    digits='Message Precision',
    help="""Price for publishing"""    
    
    )

    description = fields.Html(copy=False,help="""Very Very Long Description of 
    the required publishment.
    Maybe some insiguts
    Drafts
    or other information""")

    note = fields.Text(copy=False, help="Author Notes")

    active = fields.Boolean(default=True, help="This Message is publish or unpublish")

    publish_start_date = fields.Date(default=fields.Date.context_today,)
    

    publish_end_date = fields.Date(        
        default=fields.Date.context_today,
    )
    
    message_type = fields.Selection(string='Message Type', selection=[('adv', 'Advertising'), ('soc', 'Social'),('sec_hand', 'Second Hand')])
    
    
    
    