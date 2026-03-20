# -*- coding: utf-8 -*-
{
    'name': "rs_vehicle_delegate",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Realsystems",
    'website': "https://www.realsystems.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_auto_views.xml',
        'views/vehicle_auto_sport_views.xml',
        'views/vehicle_auto_flying_views.xml',
        'views/vehicle_auto_amphibious_views.xml',
        'views/rs_vehicle_delegate_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

