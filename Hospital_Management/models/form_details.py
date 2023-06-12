from odoo import fields, models


class FormDetails(models.Model):
    _name = "form.details"
    _inherit = ["mail.thread"]
    _description = "This model contains the details of hospital management system"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="contact")
    DOB = fields.Datetime(string="Enter your Date of Birth", required=True, help="contact")
    position = fields.Selection(
        [('doctor', 'Doctor'), ('nurse', 'Nurse'), ('receptionist', 'Receptionist'), ('clerk', 'Clerk')],
        string="Doctor", Help="contact")
    department = fields.Selection(
        [('cardiology', 'cardiologist'), ('oncology', 'oncologist'), ('psychology', 'psychologist'),
         ('dermatology', 'dermatologist')],
        string="Department", Help="contact")
