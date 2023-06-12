{
    'name': 'Hospital_Management',
    'version': '16.0.1.0.0',
    'summary': 'Hospital_Management System',
    'sequence': 10,
    'description': """
Hospital Management System
====================
This is a system that explains the complete working of hospital management including the consulatation, generating the 
Op tickets doctor's database.
    """,
    'category': 'services',
    'depends': ['contacts', 'base', 'mail', 'hr', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/tocken_op.xml',
        'data/tocken_appointment.xml',
        'data/patient_report.xml',
        'wizards/patient_report.xml',
        'views/hospital_management.xml',
        'views/contact.xml',
        'views/partner.xml',
        'views/op_ticket.xml',
        'views/consultation.xml',
        'views/disease.xml',
        'views/appointment_menu.xml',
        'views/hr_employee.xml',
        'views/menuItems.xml',
        'reports/patient_template.xml',
        'reports/report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
