from odoo import models, fields, api

class ClinicDashboard(models.Model):
    _name = "clinic.dashboard"
    _description = "TechCare Dashboard"

    # KPIs
    total_clinics = fields.Integer(string="Total Clinics", compute="_compute_dashboard_data", readonly=True, store=True)
    total_appointments = fields.Integer(string="Total Appointments", compute="_compute_dashboard_data", readonly=True, store=True)

    # Data for Charts
    appointment_trend = fields.One2many(
        'clinic.dashboard.appointment.trend',
        'dashboard_id',
        string="Appointment Trends"
    )
    clinic_appointment_distribution = fields.One2many(
        'clinic.dashboard.clinic.distribution',
        'dashboard_id',
        string="Clinic Appointment Distribution"
    )

    @api.depends()
    def _compute_dashboard_data(self):
        for record in self:
            # Count total clinics
            total_clinics = self.env['clinic.clinic'].search_count([])
            # Count total appointments
            total_appointments = self.env['clinic.appointment'].search_count([])

            record.total_clinics = total_clinics
            record.total_appointments = total_appointments

    @api.depends()
    def _compute_appointment_trend(self):
        AppointmentTrend = self.env['clinic.dashboard.appointment.trend']
        for record in self:
            # Clear old data
            record.appointment_trend = [(5, 0, 0)]
            # Fetch appointment counts grouped by date
            appointments = self.env['clinic.appointment'].read_group(
                [('date', '>=', fields.Date.today())],
                ['date:day', 'id:count'],
                ['date']
            )
            # Create trend records
            for appointment in appointments:
                AppointmentTrend.create({
                    'dashboard_id': record.id,
                    'date': appointment['date:day'],
                    'count': appointment['id_count'],
                })

    @api.depends()
    def _compute_clinic_appointment_distribution(self):
        ClinicDistribution = self.env['clinic.dashboard.clinic.distribution']
        for record in self:
            # Clear old data
            record.clinic_appointment_distribution = [(5, 0, 0)]
            # Fetch appointment counts grouped by clinic
            distribution = self.env['clinic.appointment'].read_group(
                [],
                ['clinic_id', 'id:count'],
                ['clinic_id']
            )
            # Create distribution records
            for entry in distribution:
                ClinicDistribution.create({
                    'dashboard_id': record.id,
                    'clinic_id': entry['clinic_id'][0] if entry['clinic_id'] else None,
                    'count': entry['id_count'],
                })


class ClinicDashboardAppointmentTrend(models.Model):
    _name = "clinic.dashboard.appointment.trend"
    _description = "Appointment Trend Data"

    dashboard_id = fields.Many2one('clinic.dashboard', string="Dashboard", required=True)
    date = fields.Date(string="Date", required=True)
    count = fields.Integer(string="Count", required=True)


class ClinicDashboardClinicDistribution(models.Model):
    _name = "clinic.dashboard.clinic.distribution"
    _description = "Clinic Appointment Distribution"

    dashboard_id = fields.Many2one('clinic.dashboard', string="Dashboard", required=True)
    clinic_id = fields.Many2one('clinic.clinic', string="Clinic")
    count = fields.Integer(string="Count", required=True)
