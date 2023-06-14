from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PatientReport(models.TransientModel):
    _name = "patient.report"

    patients_id = fields.Many2one('hospital.management', string="Patient")
    doct_id = fields.Many2one("hr.employee", string="Doctor", domain=[('position', '=', 'doctor')])
    token = fields.Char(string="sequence NO", help="contact")
    from_dates = fields.Datetime(string="Form Date")
    to_date = fields.Datetime(string="To Date")
    disease_id = fields.Many2one('disease.menu', string='Disease')
    department_id = fields.Many2one(string="Department", related='doct_id.department_id')

    def print_report(self):
        from_date = self.from_dates
        to_date = self.to_date
        query = """select b.patient_card_id, b.doctor_id, b.diseases_id, b.date, b.doctor_id, b.tocken,
                        a.name AS patient_name, d.name AS doctor_name, e.name AS disease_name
                        FROM op_ticket b 
                        INNER JOIN hospital_management c
                        on c.id = b.patient_card_id
                        INNER JOIN res_partner a 
                        on a.id = c.name_id
                        INNER JOIN hr_employee d
                        on d.id = b.doctor_id 
                        INNER JOIN disease_menu e
                        on e.id = b.diseases_id
                        WHERE b.date BETWEEN '%s' AND '%s' """ % (from_date, to_date)
        patients_id = self.patients_id.id
        doctor = self.doct_id.id
        disease = self.disease_id.id

        if patients_id:
            query += """AND b.patient_card_id = %s """ % patients_id
        if doctor:
            query += """AND b.doctor_id = %s """ % doctor
        if disease:
            query += """AND b.diseases_id = %s""" % disease

        self.env.cr.execute(query)
        tickets = self.env.cr.dictfetchall()
        data = {
            'form': self.read()[0],
            'ticket': tickets
        }
        return self.env.ref('Hospital_Management.report_ir_model_report').report_action(self, data=data)

    @api.constrains('from_dates', 'to_date')
    def date_constraint(self):
        for i in self:
            if i.to_date and i.from_dates:
                if i.to_date < i.from_dates:
                    raise ValidationError(_('sorry!! to date should be greater than from date'))
            else:
                raise ValidationError(_('sorry!! please enter the date to do the validate'))

    @api.model
    def create(self, vals):
        vals['token'] = self.env['ir.sequence'].next_by_code('patient.report')
        return super(PatientReport, self).create(vals)
