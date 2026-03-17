from odoo import fields, models, tools


class EstatePropertyOfferReport(models.Model):
    _name = 'estate.property.offer.report'
    _description = 'Estate Property / Offer Report'
    _auto = False
    _rec_name = 'property_id'
    _order = 'create_date DESC'

    property_id = fields.Many2one(
        comodel_name='estate.property',
        string='Property',
        readonly=True,
    )

    offer_id = fields.Many2one(
        comodel_name='estate.property.offer',
        string='Offer',
        readonly=True,
    )

    property_name = fields.Char(
        string='Property Name',
        readonly=True,
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        readonly=True,
    )

    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        readonly=True,
    )

    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string='Property Type',
        readonly=True,
    )

    expected_price = fields.Float(
        string='Expected Price',
        readonly=True,
    )

    selling_price = fields.Float(
        string='Selling Price',
        readonly=True,
    )

    offer_price = fields.Float(
        string='Offer Price',
        readonly=True,
    )

    offer_status = fields.Selection(
        string='Offer Status',
        selection=[('draft', 'New'), ('accepted', 'Acepted'),  ('reject', 'Rejected'),  ('cancel', 'Cancel')],
        default='draft',
        readonly=True,
    )

    validity = fields.Integer(
        string='Validity',
        readonly=True,
    )

    date_deadline = fields.Date(
        string='Deadline',
        readonly=True,
    )

    property_state = fields.Selection(
        selection=[('draft', 'New'),
                    ('receive', 'Offert Received'),
                    ('accepted', 'Offer Accept'),
                    ('sold', 'Sold')],
        string='Property Status',
        readonly=True,
    )

    garden = fields.Boolean(
        string='Garden',
        readonly=True,
    )

    living_area = fields.Float(
        string='Living Area',
        readonly=True,
    )

    garden_area = fields.Float(
        string='Garden Area',
        readonly=True,
    )

    total_area = fields.Float(
        string='Total Area',
        readonly=True,
    )

    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW estate_property_offer_report AS (
                SELECT
                    o.id AS id,
                    p.id AS property_id,
                    o.id AS offer_id,
                    p.name AS property_name,
                    o.partner_id AS partner_id,
                    p.user_id AS salesperson_id,
                    p.property_type_id AS property_type_id,
                    p.expected_price AS expected_price,
                    p.selling_price AS selling_price,
                    o.price AS offer_price,
                    o.state AS offer_status,
                    o.validity_days AS validity,
                    o.deadline AS date_deadline,
                    p.state AS property_state,
                    p.garden AS garden,
                    p.living_area AS living_area,
                    p.garden_area AS garden_area,
                    (COALESCE(p.living_area, 0) + COALESCE(p.garden_area, 0)) AS total_area,
                    o.create_date AS create_date
                FROM estate_property_offer o
                INNER JOIN estate_property p
                    ON o.property_id = p.id
            )
        """)
