# -*- coding: utf-8 -*-
# from odoo import http


# class RsVehicleDelegate(http.Controller):
#     @http.route('/rs_vehicle_delegate/rs_vehicle_delegate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rs_vehicle_delegate/rs_vehicle_delegate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rs_vehicle_delegate.listing', {
#             'root': '/rs_vehicle_delegate/rs_vehicle_delegate',
#             'objects': http.request.env['rs_vehicle_delegate.rs_vehicle_delegate'].search([]),
#         })

#     @http.route('/rs_vehicle_delegate/rs_vehicle_delegate/objects/<model("rs_vehicle_delegate.rs_vehicle_delegate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rs_vehicle_delegate.object', {
#             'object': obj
#         })

