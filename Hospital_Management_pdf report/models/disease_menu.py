from odoo import fields, models


class DiseaseMenu(models.Model):
    _name = "disease.menu"
    _inherit = ["mail.thread"]
    _description = "This model contains the list of different diseases"

    name = fields.Char(string="Disease Name", help="contact")
    type = fields.Selection(
        [('cardiology', 'cardiology'), ('oncology', 'oncology'), ('psychology', 'psychology'),
         ('dermatology', 'dermatology')],
        string="Type", Help="contact")
    medicines = fields.Char(String="Medicines", help="contact")
    dose = fields.Char(string="Dose", help="contact")
    days = fields.Char(string="Days", help="contact")
    description = fields.Char(string="Description", help="contact")
    treatment_id = fields.Many2one("consult.menu", string="treatment", help="contact")
