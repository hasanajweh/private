from odoo import models, fields, api

class Appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date("Date", required=True)
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Doctor", required=True)
    patient_id = fields.Many2one('clinic.patient', string="Patient", required=True)
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    notes = fields.Text("Notes")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], default='draft', tracking=True)

    schedule_id = fields.Many2one('calendar.event', string="Available Time Slot", required=True)

    def confirm_appointment(self):
        for appointment in self:
            appointment.schedule_id.write({'state': 'busy'})
            appointment.status = 'confirmed'

    def cancel_appointment(self):
        for appointment in self:
            appointment.schedule_id.write({'state': 'free'})
            appointment.status = 'canceled'

    @api.onchange('doctor_id')
    def _onchange_doctor(self):
        if self.doctor_id:
            available_times = self.env['calendar.event'].search([
                ('specialist_id', '=', self.doctor_id.id),
                ('state', '=', 'free')
            ])
            self.schedule_id = available_times[:1]
