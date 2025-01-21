from odoo import models, fields

class ClinicType(models.Model):
    _name = "clinic.type"
    _description = "Clinic Type"

    name = fields.Char(string="Clinic Type", required=True)

class AppointmentType(models.Model):
    _name = "appointment.type"
    _description = "Appointment Type"

    name = fields.Char(string="Appointment Type", required=True)

class SpecialistCategory(models.Model):
    _name = "specialist.category"
    _description = "Specialist Category"

    name = fields.Char(string="Specialist Category", required=True)
