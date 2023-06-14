from odoo import api, fields, models


class OPTicket(models.Model):
    _name = "op.ticket"
    _inherit = ["mail.thread"]
    _description = "this model contains the ticket generated"
    _rec_name = "name_id"

    patient_card_id = fields.Many2one("hospital.management", string="Patient card", help="contact")
    name_id = fields.Many2one(String="Patient Name", related='patient_card_id.name_id', help="contact")
    age = fields.Integer(String="Age", related='patient_card_id.age', help="contact")
    blood_group = fields.Selection(string="Blood Group", related='patient_card_id.blood_group', help="contact")
    gender = fields.Selection(String="Gender", related='patient_card_id.gender', help="contact")
    # doctor_id = fields.Many2one("form.details", string="Doctor", domain=[('position', '=', 'doctor')], help="contact")
    doctor_id = fields.Many2one("hr.employee", string="Doctor", domain=[('position', '=', 'doctor')])
    department_id = fields.Many2one(string="Department", related="doctor_id.department_id")
    diseases_id = fields.Many2one('disease.menu', string="Diseases")
    date = fields.Datetime(string="Date", default=lambda self: fields.datetime.now(), help="contact")
    tocken = fields.Char(string="Token NO", help="contact")
    fee = fields.Monetary(String="Fee", related='doctor_id.fee', currency_field='company_currency_id', help="contact")
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True,
                                 default=lambda self: self.env.company,
                                 help="Company related to this journal", )
    company_currency_id = fields.Many2one(string='company currency', related='company_id.currency_id', help="contact")
    state = fields.Selection([('draft', 'Draft'), ('op', 'OP')], default='draft', string='Status', readonly=True,
                             help="contact")
    invoicing_id = fields.Many2one('account.move', String='connection', help='contact')
    boolean_field = fields.Boolean(string="Ribbon", compute='_compute_boolean_field', store=True, default=False)

    @api.model
    def create(self, vals):
        vals['tocken'] = self.env['ir.sequence'].next_by_code('op.ticket')
        return super(OPTicket, self).create(vals)

    def action_confirm(self):
        self.state = 'op'

    def fee_payment(self):
        invoice = self.invoicing_id.create(
            {
                'move_type': 'out_invoice',
                'partner_id': self.name_id.id,
                'state': 'draft',
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [
                    (0, 0, {'name': 'consultation fee for doctor',
                            'price_unit': self.fee})]
            }
        )
        self.invoicing_id = invoice.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'move_type': 'out_invoice',
            'res_id': invoice.id,
            'target': 'current'
        }

    @api.depends('invoicing_id.state')
    def _compute_boolean_field(self):
        for i in self:
            if i.invoicing_id:
                if i.invoicing_id.state == 'posted':
                    i.boolean_field = True
            else:
                i.boolean_field = False
