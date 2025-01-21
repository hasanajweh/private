from odoo import models, fields, api

class Clinic(models.Model):
    _name = 'clinic.clinic'
    _description = 'Clinic'

    name = fields.Char("Clinic Name", required=True)
    address = fields.Char("Address")
    contact_info = fields.Char("Contact Information")
    doctors = fields.One2many('clinic.medical_specialist', 'clinic_id', string="Doctors")
    patients = fields.One2many('clinic.patient', 'clinic_id', string="Patients")
    total_patients = fields.Integer("Total Patients", compute="_compute_total_patients", store=True)
    clinic_type_id = fields.Many2one('clinic.type', string="Clinic Type")  # New field

    @api.depends('patients')
    def _compute_total_patients(self):
        for record in self:
            record.total_patients = len(record.patients)