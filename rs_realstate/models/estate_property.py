from odoo import models,fields,api,_
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'

    _inherit = ['mail.thread','mail.activity.mixin']

    _rec_name = 'name'
    _order = 'name ASC'


    def _default_currency_id(self):
        return self.env.user.company_id.currency_id


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('estate.property') or _('New')
        return super().create(vals_list)

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
    living_area = fields.Integer(string='Living Area [m2]',tracking=True)

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
        tracking=True,
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
        tracking=True,)
    
    salesman_name = fields.Char(
        related="user_id.display_name"
    )
    
    

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

    garden_area = fields.Integer(string='Garden Area [m2]')

    total_area = fields.Integer(
            string='Total Area [m²]',
            compute='_compute_total_area',
            store=True
        )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_open_estate_property_offers(self):
        context = self.env.context

        if context.get('my_flag'):
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
        else:
            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'This is a MEssage Test',
                'message': 'My Flag is False se ejecutó correctamente.',
                'type': 'success',
                'sticky': False,
            }
        }


    def action_sold(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("This property is already sold."))

            offer_states = record.offer_ids.mapped('state')

            if 'accepted' not in offer_states:
                raise UserError(
                    _("You cannot sell a property without an accepted offer.")
                )

            record.state = 'sold'




    def write(self, values):
        """
            Update all record(s) in recordset, with new value comes as {values}
            return True on success, False otherwise

            @param values: dict of new values to be set

            @return: True on success, False otherwise
        """

        result = super().write(values)

        return result

    def action_update_property_state(self):
        for rec in self:
            accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', rec.id),
                ('state', '=', 'accepted'),
            ], limit=1)

            if accepted_offer:
                rec.state = 'accepted'

    def action_update_property_state_sold(self,message_by=None):
        for rec in self:
            accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', rec.id),
                ('state', '=', 'sold'),
            ], limit=1)
            #import wdb;wdb.set_trace()

            if accepted_offer:
                rec.state = 'sold'
                rec.message_post(
                    body=_(
                        "🏁 Property SOLD via offer from \n%s\n for \n%s %s\n %s"
                    ) % (
                        accepted_offer.partner_id.display_name,
                        accepted_offer.price,
                        accepted_offer.currency_id.name,
                        message_by or '',
                    )
                )


    def action_update_property_state_sold_cron(self):
        records = self.env['estate.property'].search([
                ('state', '=', 'accepted'),
            ], limit=1)
        for rec in records:
            accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', rec.id),
                ('state', '=', 'sold'),
            ], limit=1)

            if accepted_offer:
                rec.state = 'sold'


    @api.depends('name', 'partner_id', 'property_type_id')
    def _compute_display_name(self):
        for rec in self:
            parts = [
                f"[{rec.name}]"
                ]

            if rec.partner_id:
                parts.append(rec.partner_id.name)

            if rec.property_type_id:
                parts.append(rec.property_type_id.name)

            rec.display_name = " - ".join(parts)

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(
                    _("Only properties in status 'New' can be deleted.")
                )

            if rec.offer_ids:
                raise UserError(
                    _("You cannot delete a property that has offers.")
                )

        return super().unlink()


    def read(self, fields=None, load='_classic_read'):
        result = super().read(fields, load=load)

        for rec in self:
            _logger = self.env['ir.logging']
            self.env.user
            _logger.create({
                'name': 'estate.property.read',
                'type': 'server',
                'level': 'INFO',
                'message': f"Property viewed: {rec.name} by {self.env.user.name} what ammazing",
                'path': 'estate.property',
                'func': 'read',
                'line': '0',
            })

        return result

    def action_send_email(self):
        self.ensure_one()

        template = self.env.ref(
            'rs_realstate.mail_template_estate_property',
            raise_if_not_found=False
        )

        ctx = {
            'default_model': 'estate.property',
            'default_res_ids': self.ids,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'email_notification_allow_footer': True,
            'force_email': True,
            'model_description': _('Property'),
        }

        if template:
            ctx.update({
                'default_template_id': template.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_send_mail_direct(self):
        self.ensure_one()
        template = self.env.ref('rs_realstate.mail_template_estate_property')
        lang = (
                (self.partner_id.lang if self.partner_id else False)
                or (self.user_id.lang if self.user_id else False)
                or (self.company_id.partner_id.lang if self.company_id and self.company_id.partner_id else False)
                or self.env.lang
                or 'en_US'
                )
        template.with_context(lang=lang).send_mail(self.id, force_send=True)
