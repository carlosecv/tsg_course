from odoo import models,fields,api,_
from datetime import timedelta

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

    validity_days = fields.Integer(string='Validity Days',
        compute='_compute_validity',
        inverse='_inverse_validity',
        store=True
    )

    deadline  = fields.Date(string='Deadline',
                    compute='_compute_validity',
                    inverse='_inverse_deadline',
                    store=True
    )

    # ===============================
    # COMPUTE
    # ===============================

    @api.depends('create_date', 'validity_days')
    def _compute_validity(self):
        for record in self:
            if record.create_date and record.validity_days:
                base_date = record.create_date.date()
                record.deadline = base_date + timedelta(days=record.validity_days)
            else:
                record.deadline = False

    # ===============================
    # INVERSE (cuando cambias deadline)
    # ===============================

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.deadline:
                base_date = record.create_date.date()
                delta = record.deadline - base_date
                record.validity_days = delta.days
    
    # ===============================
    # INVERSE (cuando cambias validity_days)
    # ===============================

    def _inverse_validity(self):
        for record in self:
            if record.create_date and record.validity_days:
                base_date = record.create_date.date()
                record.deadline = base_date + timedelta(days=record.validity_days)
    
    sequence = fields.Integer(string='Sequence')
    
    
    elapsed_days = fields.Integer(string='Elapsed Days',
            compute='_compute_elapsed_days')
            
    @api.depends('create_date')
    def _compute_elapsed_days(self):
        today = fields.Date.today()
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
                record.elapsed_days = (today - create_date).days
            else:
                record.elapsed_days = 0
                
        
        
        

    