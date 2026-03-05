from odoo import models,fields,api,_
from datetime import timedelta
from odoo.exceptions import ValidationError,UserError

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

    
    @api.model_create_multi
    def create(self, vals_list):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        for values in vals_list:
            if values.get('deadline',None):                
                create_date = fields.Date.today()
                days = fields.Date.to_date(values.get('deadline')) - create_date
                if days.days > 30:                    
                    raise UserError("USERROR create: The validity days must be less than 30 days")
                    raise ValidationError("VALERR create: The validity days must be less than 30 days")

        result = super().create(values)
    
        return result
    
        
    def write(self, values):
        """
            Update all record(s) in recordset, with new value comes as {values}
            return True on success, False otherwise
    
            @param values: dict of new values to be set
    
            @return: True on success, False otherwise
        """        
        for rec in self:
            if values.get('deadline',None):
                days = fields.Date.to_date(values.get('deadline')) - rec.create_date.date()
                if days.days > 30:                    
                    raise UserError("USERROR write: The validity days must be less than 30 days")
                    raise ValidationError("VALERR write: The validity days must be less than 30 days")
                    
        
        result = super().write(values)
    
        return result
    

    @api.onchange('validity_days','deadline')
    def _onchange_validity_days(self):
        if self.validity_days > 30:
            raise UserError("USERROR Onchange: The validity days must be less than 30 days")
            raise ValidationError("Onchange The validity days must be less than 30 days")
    
    

    @api.constrains('price','currency_id')
    def _check_price(self):
        user_currency = self.env.user.company_id.currency_id
        company_id = self.env.user.company_id
        minimal_price=self.env['ir.config_parameter'].sudo().search([('key','=','minimum_property_offer_value')])
        if not minimal_price:
            return
        for record in self:            
            converted_price = record.currency_id._convert(record.price, user_currency, company_id, record.create_date.date(), round=2)           
            if converted_price < float(minimal_price.value):
                raise ValidationError(f"The price must be greater than {minimal_price.value} {user_currency.name}")

    def message_user(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Éxito',
                'message': 'La acción se ejecutó correctamente.',
                'type': 'success',
                'sticky': False,
            }
        }

#     _sql_constraints = [
#         ('check_base_price_min', 'CHECK ( price >= 200000.0)',
# 'The Price must be minimum 200000'),
#     ]
    
        
        
    
    