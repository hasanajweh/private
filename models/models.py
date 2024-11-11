from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Clinic(models.Model):
    _name = 'clinic.clinic'
    _description = 'Clinic'

    name = fields.Char("Clinic Name", required=True)
    address = fields.Char("Address")
    contact_info = fields.Char("Contact Information")
    doctors = fields.One2many('clinic.medical_specialist', 'clinic_id', string="Doctors")
    patients = fields.One2many('clinic.patient', 'clinic_id', string="Patients")


class MedicalSpecialist(models.Model):
    _name = 'clinic.medical_specialist'
    _description = 'Medical Specialist'

    name = fields.Char("Doctor Name", required=True)
    specialization = fields.Char("Specialization")
    contact_info = fields.Char("Contact Information")
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    available_times = fields.One2many('calendar.event', 'specialist_id',
                                      string="Available Times")  # Linking calendar events for availability


class Patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient'

    name = fields.Char("Patient Name", required=True)
    id_number = fields.Char("ID Number", required=True)
    birth_date = fields.Date("Birth Date")
    age = fields.Integer("Age", compute="_compute_age", store=True)
    medical_history = fields.Text("Medical History")
    emergency_contact = fields.Char("Emergency Contact")  # New field for emergency contact
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = (fields.Date.today() - record.birth_date).days // 365
            else:
                record.age = 0


class Appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enables chat functionality

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
    ], default='draft', tracking=True)  # Added tracking for appointment status changes

    # New field to reference calendar event for available times
    schedule_id = fields.Many2one('calendar.event', string="Available Time Slot", required=True)

    def confirm_appointment(self):
        """Method to confirm appointment status"""
        for appointment in self:
            # Mark the selected schedule as booked when the appointment is confirmed
            appointment.schedule_id.write({'state': 'busy'})  # Mark calendar event as busy
            appointment.status = 'confirmed'

    def cancel_appointment(self):
        """Method to cancel appointment"""
        for appointment in self:
            # Optionally reset the state of the calendar event back to available
            appointment.schedule_id.write({'state': 'free'})
            appointment.status = 'canceled'

    @api.onchange('doctor_id')
    def _onchange_doctor(self):
        if self.doctor_id:
            # Filter calendar events to only show available slots for the selected doctor
            available_times = self.env['calendar.event'].search([
                ('specialist_id', '=', self.doctor_id.id),
                ('state', '=', 'free')  # Only show available slots
            ])
            self.schedule_id = available_times[:1]  # Automatically select the first available slot if any


class Announcement(models.Model):
    _name = 'clinic.announcement'
    _description = 'Announcement'

    title = fields.Char("Title", required=True)
    content = fields.Text("Content")
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Doctor")
    created_date = fields.Datetime("Created Date", default=fields.Datetime.now)
    expiry_date = fields.Datetime("Expiry Date")



class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    specialist_id = fields.Many2one('clinic.medical_specialist', string="Specialist")
    state = fields.Selection([
        ('free', 'Free'),
        ('busy', 'Busy')
    ], default='free', string="State")

