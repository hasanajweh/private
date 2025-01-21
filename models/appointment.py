from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Only keep these if you need chatter.

    clinic_id = fields.Many2one('clinic.clinic', string="Clinic", required=True)
    doctor_id = fields.Many2one(
        'clinic.medical_specialist', string="Medical Specialist", required=True, domain="[('clinic_id', '=', clinic_id)]"
    )
    date = fields.Datetime(string="Appointment Date", required=True)
    time = fields.Float(string="Time", required=True, help="Time in hours (e.g., 14.5 for 2:30 PM)")
    patient_id = fields.Many2one(
        'clinic.patient', string="Patient", required=True, domain="[('clinic_id', '=', clinic_id)]"
    )
    status = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('canceled', 'Canceled')],
        default='draft', string="Status", tracking=True
    )

    @api.constrains('date')
    def _check_date(self):
        """Ensure the appointment date is not in the past."""
        for record in self:
            if record.date and record.date < fields.Datetime.now():
                raise ValidationError("The appointment date cannot be in the past.")
