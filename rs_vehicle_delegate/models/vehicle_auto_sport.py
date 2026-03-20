from odoo import models, fields

class VehicleAutoSport(models.Model):
    _name = 'vehicle.auto.sport'
    _description = 'Sport Auto'
    _inherits = {'vehicle.auto': 'auto_id'}

    auto_id = fields.Many2one(
        comodel_name='vehicle.auto',
        string='Base Auto',
        required=True,
        ondelete='cascade',
    )

    acceleration_0_100 = fields.Float(string='0 to 100 km/h (s)')
    traction_type = fields.Selection(
        selection=[
            ('fwd', 'Front-Wheel Drive'),
            ('rwd', 'Rear-Wheel Drive'),
            ('awd', 'All-Wheel Drive'),
        ],
        string='Traction Type',
    )
    turbo_mode = fields.Boolean(string='Turbo Mode')