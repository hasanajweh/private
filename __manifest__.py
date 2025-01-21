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
        'views/clinic_views.xml',
        'views/techcare_views.xml',
        'views/configuration_views.xml',
        'views/dashboard.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}
