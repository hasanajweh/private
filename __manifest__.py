{
    'name': 'TechCare',
    'version': '1.0',
    'summary': 'Connecting Medical Specialists with the Community',
    'category': 'Medical/Medical',
    'author': 'Hasan Ajweh',
    'depends': ['base', 'mail', 'calendar', 'website'],
    'data': [
        'security/techcare_security.xml',
        'security/ir.model.access.csv',
        'views/techcare_views.xml',
    ],
    'installable': True,
    'application': True,
}
