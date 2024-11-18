from odoo import models, fields, api

class Patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient'

    name = fields.Char("Patient Name", required=True)
    id_number = fields.Char("ID Number", required=True)
    birth_date = fields.Date("Birth Date")
    age = fields.Integer("Age", compute="_compute_age", store=True)
    medical_history = fields.Text("Medical History")
    emergency_contact = fields.Char("Emergency Contact")
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    user_id = fields.Many2one('res.users', string="Related User", help="System user linked to this patient.")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = (fields.Date.today() - record.birth_date).days // 365
            else:
                record.age = 0
