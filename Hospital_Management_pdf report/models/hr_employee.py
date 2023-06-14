from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    position = fields.Selection([('doctor', 'Doctor'), ('clerk', 'Clerk'), ('receptionist', 'Receptionist')],
                                string="Job Position",
                                help="contact")
    fee = fields.Monetary(String="Fee", currency_field='company_currency_id', help="contact")
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True,
                                 default=lambda self: self.env.company,
                                 help="Company related to this journal", )
    company_currency_id = fields.Many2one(string='company currency', related='company_id.currency_id', help="contact")
