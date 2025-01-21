from odoo import models, fields, api

class Announcement(models.Model):
    _name = 'clinic.announcement'
    _description = 'Announcement'

    title = fields.Char("Title", required=True)
    content = fields.Text("Content", required=True)
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Targeted Medical Specialist")
    clinic_id = fields.Many2one('clinic.clinic', string="Targeted Clinic")
    created_date = fields.Datetime("Created Date", default=fields.Datetime.now)
    expiry_date = fields.Datetime("Expiry Date")
    is_expired = fields.Boolean("Is Expired", compute="_compute_is_expired", store=True)

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        for record in self:
            record.is_expired = record.expiry_date and record.expiry_date < fields.Datetime.now()