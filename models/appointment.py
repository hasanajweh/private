from odoo import models, fields, api

class Appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Datetime("Appointment Date", required=True, tracking=True)
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Medical Specialist", required=True)
    patient_id = fields.Many2one(
        'clinic.patient',
        string="Patient",
        required=True,
        default=lambda self: self._get_default_patient()
    )
    notes = fields.Text("Notes")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], default='draft', tracking=True)

    @api.model
    def _get_default_patient(self):
        """Get the default patient record for the logged-in user."""
        return self.env['clinic.patient'].search([('id_number', '=', self.env.user.partner_id.id)], limit=1).id

    def confirm_appointment(self):
        """Method to confirm the appointment."""
        self.status = 'confirmed'

    def cancel_appointment(self):
        """Method to cancel the appointment."""
        self.status = 'canceled'

    def mark_done(self):
        """Method to mark the appointment as done."""
        self.status = 'done'
