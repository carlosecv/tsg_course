from odoo import models, fields


class VehicleAutoFlying(models.Model):
    _name = 'vehicle.auto.flying'
    _description = 'Flying Auto'
    _inherits = {'vehicle.auto': 'auto_id'}

    auto_id = fields.Many2one(
        comodel_name='vehicle.auto',
        string='Base Auto',
        required=True,
        ondelete='cascade',
    )

    max_altitude = fields.Float(string='Max Altitude (m)')
    flight_range = fields.Float(string='Flight Range (km)')
    pilot_license_required = fields.Boolean(string='Pilot License Required')