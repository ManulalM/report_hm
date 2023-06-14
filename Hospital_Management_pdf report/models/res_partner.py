from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender",
                              help="contact")
    dob = fields.Date(String="DOB")
