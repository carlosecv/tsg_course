from odoo import models, fields


class VehicleAutoAmphibious(models.Model):
    _name = 'vehicle.auto.amphibious'
    _description = 'Amphibious Auto'
    _inherits = {'vehicle.auto': 'auto_id'}

    auto_id = fields.Many2one(
        comodel_name='vehicle.auto',
        string='Base Auto',
        required=True,
        ondelete='cascade',
    )

    water_speed = fields.Float(string='Water Speed (km/h)')
    max_depth = fields.Float(string='Max Depth (m)')
    propeller_mode = fields.Boolean(string='Propeller Mode')