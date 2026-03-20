from odoo import models, fields, api, _


class VehicleAuto(models.Model):
    _name = 'vehicle.auto'
    _description = 'Auto'
    _rec_name = 'display_name'
    _order = 'brand, model_name, year desc'

    name = fields.Char(
        string='Reference',
        required=True,
        default=lambda self: _('New'),
        copy=False,
    )

    brand = fields.Char(string='Brand', required=True)
    model_name = fields.Char(string='Model', required=True)
    year = fields.Integer(string='Year')
    color = fields.Char(string='Color')
    max_speed = fields.Float(string='Max Speed (km/h)')
    active = fields.Boolean(string='Active', default=True)

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
    )

    @api.depends('brand', 'model_name', 'year')
    def _compute_display_name(self):
        for record in self:
            parts = [record.brand or '', record.model_name or '']
            if record.year:
                parts.append(str(record.year))
            record.display_name = ' '.join([p for p in parts if p]).strip() or _('New Auto')