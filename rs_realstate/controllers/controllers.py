# -*- coding: utf-8 -*-
# from odoo import http


# class RsRealstate(http.Controller):
#     @http.route('/rs_realstate/rs_realstate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rs_realstate/rs_realstate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rs_realstate.listing', {
#             'root': '/rs_realstate/rs_realstate',
#             'objects': http.request.env['rs_realstate.rs_realstate'].search([]),
#         })

#     @http.route('/rs_realstate/rs_realstate/objects/<model("rs_realstate.rs_realstate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rs_realstate.object', {
#             'object': obj
#         })

