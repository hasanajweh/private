{
    'name': 'TechCare',
    'version': '1.0',
    'summary': 'Clinics System',
    'category': 'Medical/Medical',
    'author': 'Hasan Ajweh',
    'depends': ['base', 'mail', 'calendar', 'website'],
    'data': [
        'security/techcare_security.xml',
        'security/ir.model.access.csv',
        'views/techcare_views.xml',
        'views/menus.xml',  # menus
    ],
    'installable': True,
    'application': True,
}
