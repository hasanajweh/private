from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
        """
        Validates Palestinian ID numbers using parity check logic.
        """
        if not id_number or not id_number.isdigit() or len(id_number) != 9:  # Ensure the input is a 9-digit number
            return False

        # Convert ID to a list of integers for processing
        digits = list(map(int, id_number))
        r = 0  # The running total for the checksum

        # Apply the parity check logic
        for idx, digit in enumerate(digits[:-1]):  # Skip the last digit (check digit)
            if idx % 2 == 0:  # Even-indexed positions (0-based)
                r += digit
            else:  # Odd-indexed positions
                doubled = digit * 2
                r += doubled if doubled < 10 else (doubled // 10 + doubled % 10)  # Sum the digits of doubled value

        # Calculate the check digit
        next_multiple_of_10 = (r + 9) // 10 * 10
        calculated_check_digit = next_multiple_of_10 - r

        # Validate against the actual check digit (last digit)
        return calculated_check_digit == digits[-1]

    @api.constrains('id_number')
    def _check_valid_id(self):
        for record in self:
            if not self._check_id_parity(record.id_number):
                raise ValidationError("The ID Number is invalid. Please enter a valid Palestinian ID.")

