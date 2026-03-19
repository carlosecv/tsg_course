from odoo import http
from odoo.http import request


class EstatePropertyApi(http.Controller):

    @http.route(
        '/api/estate/properties/available',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def get_available_properties(self, **kwargs):
        # Si "receive" en tu modelo realmente se llama distinto
        # cámbialo aquí, por ejemplo por "received"
        domain = [
            ('state', 'in', ['draft', 'receive'])
        ]

        properties = request.env['estate.property'].sudo().search(domain)

        result = []
        for prop in properties:
            result.append({
                'id': prop.id,
                'name': prop.name,
                'expected_price': prop.expected_price,
                'selling_price': prop.selling_price,
                'state': prop.state,
                'bedrooms': prop.bedrooms,
                'living_area': prop.living_area,
                'facades': prop.facades,
                'garage': prop.garage,
                'garden': prop.garden,
                'garden_area': prop.garden_area,
                'postcode': prop.postcode,
                'date_availability': str(prop.date_availability) if prop.date_availability else False,
                'property_type': prop.property_type_id.name if prop.property_type_id else False,
                'salesman': prop.salesman_id.name if prop.salesman_id else False,
                'buyer': prop.buyer_id.name if prop.buyer_id else False,
            })

        return {
            'count': len(result),
            'results': result,
        }