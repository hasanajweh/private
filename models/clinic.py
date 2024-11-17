from odoo import models, fields

class Clinic(models.Model):
    _name = 'clinic.clinic'
    _description = 'Clinic'

    name = fields.Char("Clinic Name", required=True)
    address = fields.Char("Address")
    contact_info = fields.Char("Contact Information")
    doctors = fields.One2many('clinic.medical_specialist', 'clinic_id', string="Doctors")
    patients = fields.One2many('clinic.patient', 'clinic_id', string="Patients")
