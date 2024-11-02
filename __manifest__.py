{
    'name': 'TechCare',
    'version': '1.0',
    'summary': 'Connecting Medical Specialists with the Community',
    'category': 'Medical',
    'author': 'Hasan Ajweh',
    'depends': ['base', 'mail', 'calendar', 'website',],
    'data': [
        'security/techcare_security.xml',     # Security groups
        'security/ir.model.access.csv',       # Security access
        'views/techcare_views.xml',           # Views file
    ],
    'installable': True,
    'application': True,
}
