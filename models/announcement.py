from odoo import models, fields

class Announcement(models.Model):
    _name = 'clinic.announcement'
    _description = 'Announcement'

    title = fields.Char("Title", required=True)
    content = fields.Text("Content", required=True)
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Targeted Medical Specialist")
    clinic_id = fields.Many2one('clinic.clinic', string="Targeted Clinic")
    created_date = fields.Datetime("Created Date", default=fields.Datetime.now)
    expiry_date = fields.Datetime("Expiry Date")
