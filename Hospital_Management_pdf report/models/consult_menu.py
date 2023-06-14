from odoo import fields, models


class ConsultMenu(models.Model):
    _name = "consult.menu"
    _inherit = ["mail.thread"]
    _description = "this model contains the consultation details"
    _rec_name = "patients_id"

    patients_id = fields.Many2one("hospital.management", string="Patient card", help="contact")
    type = fields.Selection([('op', 'OP'), ('ip', 'IP')], string="Consultation Type", Help="contact")
    doctor_id = fields.Many2one("hr.employee", string="Doctor", domain=[('position', '=', 'doctor')])
    departments_id = fields.Many2one(string="Department", related="doctor_id.department_id", help="contact")
    date = fields.Datetime(string="Date", default=lambda self: fields.datetime.now(), help="contact")
    disease_id = fields.Many2one("disease.menu", string="Disease", help="contact")
    diagnose = fields.Text(string="Diagnose", help="contact")
    treatment1_ids = fields.One2many("disease.menu", "treatment_id", string="Treat", help="contact")



