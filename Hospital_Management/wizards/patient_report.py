from odoo import api, fields, models


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
        if patients_id:
            query += """AND b.patient_card_id = %s """ % patients_id
        doctor = self.doct_id.id
        if doctor:
            query += """AND b.doctor_id = %s """ % doctor
        # dept = self.department_id.id
        # if dept:
        #     query += """AND b.department_id = %s """ % dept
        disease = self.disease_id.id
        if disease:
            query += """AND b.diseases_id = %s""" % disease
        self.env.cr.execute(query)
        tickets = self.env.cr.dictfetchall()
        print('sql', tickets)
        op = self.env['op.ticket'].search_read()
        print("form", self.read()[0])
        print("op", op)
        data = {
            'form': self.read()[0],
            'ticket': tickets
        }
        return self.env.ref('Hospital_Management.report_ir_model_report').report_action(self, data=data)

    @api.model
    def create(self, vals):
        vals['token'] = self.env['ir.sequence'].next_by_code('patient.report')
        return super(PatientReport, self).create(vals)
