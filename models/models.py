from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

# Clinic model
class Clinic(models.Model):
    _name = 'clinic.clinic'
    _description = 'Clinic'

    name = fields.Char("Clinic Name", required=True)
    address = fields.Char("Address")
    contact_info = fields.Char("Contact Information")
    doctors = fields.One2many('clinic.medical_specialist', 'clinic_id', string="Doctors")
    patients = fields.One2many('clinic.patient', 'clinic_id', string="Patients")


# Medical Specialist model
class MedicalSpecialist(models.Model):
    _name = 'clinic.medical_specialist'
    _description = 'Medical Specialist'

    name = fields.Char("Doctor Name", required=True)
    specialization = fields.Char("Specialization")
    contact_info = fields.Char("Contact Information")
    availability_schedule = fields.Text("Availability Schedule")
    user_id = fields.Many2one('res.users', string="Related User")
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    appointments = fields.One2many('clinic.appointment', 'doctor_id', string="Appointments")
    announcements = fields.One2many('clinic.announcement', 'doctor_id', string="Announcements")


# Patient model with parity check
class Patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient'

    name = fields.Char("Patient Name", required=True)
    id_number = fields.Char("ID Number", required=True)
    contact_info = fields.Char("Contact Information")
    date_of_birth = fields.Date("Date of Birth")
    medical_history = fields.Text("Medical History")
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    appointments = fields.One2many('clinic.appointment', 'patient_id', string="Appointments")

    @api.constrains('id_number')
    def check_id_parity(self):
        for patient in self:
            if not self._validate_id_number(patient.id_number):
                raise ValidationError(_("Invalid ID Number. Please check and try again."))

    def _validate_id_number(self, id_number):
        if len(id_number) != 10 or not id_number.isdigit():
            return False
        # Simple parity check: sum of even indexed digits should equal sum of odd indexed digits
        return sum(int(id_number[i]) for i in range(0, len(id_number), 2)) == sum(int(id_number[i]) for i in range(1, len(id_number), 2))


# Appointment model
class Appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'

    date = fields.Date("Date", required=True)
    time = fields.Float("Time", required=True)
    status = fields.Selection([
        ('upcoming', "Upcoming"),
        ('completed', "Completed"),
        ('canceled', "Canceled")
    ], default='upcoming')
    description = fields.Text("Description")
    prescription = fields.Text("Prescription")
    notes = fields.Text("Notes")
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Doctor", required=True)
    patient_id = fields.Many2one('clinic.patient', string="Patient", required=True)
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")


# Announcement model
class Announcement(models.Model):
    _name = 'clinic.announcement'
    _description = 'Announcement'

    title = fields.Char("Title", required=True)
    content = fields.Text("Content")
    created_date = fields.Date("Created Date", default=fields.Date.today)
    expiry_date = fields.Date("Expiry Date")
    date = fields.Date("Date")
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Doctor")
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
