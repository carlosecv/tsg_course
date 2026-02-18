
{
    'name': 'Hello World Module',
    'summary': 'This is a demostration First Module',
    'version': '1.0',

    'description': """
Hello World Module.
==============================================
  * This is a demostration First Module

    """,

    'author': 'Real Systems',
    'maintainer': 'Carlos Contreras <carlosecv@realsystems.com.mx>',
    'contributors': [],
    'website': 'http://www.github.com/carlosecv/tsg_course.git',

    'license': 'AGPL-3',
    'category': 'Customization',

    'depends': [
        'base'
    ],
    'external_dependencies': {
        'python': [
        ],
    },
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/decimal_precision_data.xml',
        'views/rs_hello_views.xml',
        
        'views/rs_helloworld_menus.xml',


    ],
    'demo': [
    ],
    'js': [
    ],
    'css': [
    ],
    'qweb': [
    ],
    'images': [
    ],
    'test': [
    ],
    'application': False,
    'installable': True
}
