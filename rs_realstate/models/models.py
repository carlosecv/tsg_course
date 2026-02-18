# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rs_realstate(models.Model):
#     _name = 'rs_realstate.rs_realstate'
#     _description = 'rs_realstate.rs_realstate'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

