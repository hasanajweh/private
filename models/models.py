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

class Patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient'

    name = fields.Char("Patient Name", required=True)
    id_number = fields.Char("ID Number", required=True)
    birth_date = fields.Date("Birth Date")
    medical_history = fields.Text("Medical History")
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")

class Appointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Appointment'

    date = fields.Date("Date", required=True)
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Doctor", required=True)
    patient_id = fields.Many2one('clinic.patient', string="Patient", required=True)
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    notes = fields.Text("Notes")

class Announcement(models.Model):
    _name = 'clinic.announcement'
    _description = 'Announcement'

    title = fields.Char("Title", required=True)
    content = fields.Text("Content")
    doctor_id = fields.Many2one('clinic.medical_specialist', string="Doctor")
    created_date = fields.Datetime("Created Date",default=fields.Datetime.now)
    expiry_date = fields.Datetime("Expiry Date")
