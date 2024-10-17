from odoo import models, fields

class TechCareAnnouncement(models.Model):
    _name = 'techcare.announcement'
    _description = 'TechCare Announcement'

    title = fields.Char(string='Title', required=True)
    content = fields.Text(string='Content')
    date_posted = fields.Datetime(string='Date Posted', default=fields.Datetime.now)
    is_active = fields.Boolean(string='Active', default=True)
    specialist_id = fields.Many2one('res.users', string='Medical Specialist', required=True)

class TechCareAppointment(models.Model):
    _name = 'techcare.appointment'
    _description = 'TechCare Appointment'

    patient_name = fields.Char(string='Patient Name', required=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    specialist_id = fields.Many2one('res.users', string='Medical Specialist', required=True)
    notes = fields.Text(string='Notes')
    is_confirmed = fields.Boolean(string='Confirmed', default=False)

    def confirm_appointment(self):
        self.is_confirmed = True
        # Send email notification
        template = self.env.ref('techcare.email_template_appointment_confirmation')
        template.send_mail(self.id, force_send=True)

    def create_calendar_event(self):
        event_vals = {
            'name': self.patient_name,
            'start': self.appointment_date,
            'stop': self.appointment_date + timedelta(hours=1),  # Assuming 1-hour appointment
            'user_id': self.specialist_id.id,
        }
        self.env['calendar.event'].create(event_vals)

class TechCareComment(models.Model):
    _name = 'techcare.comment'
    _description = 'TechCare Comment'

    announcement_id = fields.Many2one('techcare.announcement', string='Announcement', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    content = fields.Text(string='Comment', required=True)
