from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient'

    name = fields.Char("Patient Name", required=True)
    id_number = fields.Char("ID Number", required=True)
    birth_date = fields.Date("Birth Date")
    medical_history = fields.Text("Medical History")
    emergency_contact = fields.Char("Emergency Contact")
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    user_id = fields.Many2one('res.users', string="Related User", help="System user linked to this patient.")
    is_id_valid = fields.Boolean("Is ID Number Valid", compute="_compute_is_id_valid", store=True)

    @api.depends('id_number')
    def _compute_is_id_valid(self):
        for record in self:
            record.is_id_valid = self._check_id_parity(record.id_number)

    def _check_id_parity(self, id_number):
        if not id_number or not id_number.isdigit() or len(id_number) != 9:
            return False

        digits = list(map(int, id_number))
        r = 0

        for idx, digit in enumerate(digits[:-1]):
            if idx % 2 == 0:
                r += digit
            else:
                doubled = digit * 2
                r += doubled if doubled < 10 else (doubled // 10 + doubled % 10)

        next_multiple_of_10 = (r + 9) // 10 * 10
        calculated_check_digit = next_multiple_of_10 - r

        return calculated_check_digit == digits[-1]

    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Ensure that birth_date is not in the future."""
        for record in self:
            if record.birth_date and record.birth_date > date.today():
                raise ValidationError("The Birth Date cannot be in the future.")
