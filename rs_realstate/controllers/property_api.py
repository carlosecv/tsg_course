from odoo import http
from odoo.http import request
import json


class EstatePropertyApi(http.Controller):

    @http.route('/test_api_rs', type='http', auth='public', methods=['GET'], csrf=False)
    def test_api_rs(self, **kwargs):
        return http.Response("API OK", content_type="text/plain")

    @http.route('/api/estate/properties/available/http', type='http', auth='public', methods=['GET'], csrf=False)
    def get_available_properties_http(self, **kwargs):
        properties = request.env['estate.property'].sudo().search([
            ('state', 'in', ['draft', 'receive'])
        ])

        results = []
        for prop in properties:
            results.append({
                'id': prop.id,
                'name': prop.name,
                'state': prop.state,
                'expected_price': prop.expected_price,
                'selling_price': prop.selling_price,
            })

        return http.Response(
            json.dumps({
                'count': len(results),
                'results': results,
            }),
            content_type='application/json'
        )