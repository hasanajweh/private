from odoo import models, fields, api

class MedicalSpecialist(models.Model):
    _name = 'clinic.medical_specialist'
    _description = 'Medical Specialist'

    name = fields.Char("Doctor Name", required=True)
    specialization = fields.Char("Specialization")
    contact_info = fields.Char("Contact Information")
    clinic_id = fields.Many2one('clinic.clinic', string="Assigned Clinic", required=True)
    available_times = fields.One2many('calendar.event', 'specialist_id', string="Available Times")
