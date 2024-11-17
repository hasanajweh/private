from odoo import models, fields

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    specialist_id = fields.Many2one('clinic.medical_specialist', string="Specialist")
    state = fields.Selection([
        ('free', 'Free'),
        ('busy', 'Busy')
    ], default='free', string="State")
