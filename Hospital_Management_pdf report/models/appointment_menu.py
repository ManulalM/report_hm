from odoo import api, fields, models


class AppointmentMenu(models.Model):
    _name = "appointment.menu"
    _inherit = ["mail.thread"]
    _description = "This model contains the details of all the appointments scheduled for  hospital management system"
    _rec_name = "patientname"

    patientcard_id = fields.Many2one("hospital.management", string="Patient card", help="contact")
    patientname = fields.Many2one(string="Patient Name", related="patientcard_id.name_id")
    doctorname_id = fields.Many2one("hr.employee", string="Doctor", domain=[('position', '=', 'doctor')])
    departmentname_id = fields.Many2one(string="Department", related="doctorname_id.department_id", help="contact")
    datei = fields.Datetime(string="Date", default=lambda self: fields.datetime.now(), help="contact")
    tockens = fields.Char(string="Tocken", help='contact')
    state = fields.Selection([('draft', 'Draft'), ('appointment', 'Appointment'), ('op', 'OP')], default='draft',
                             string='Status',
                             readonly=True,
                             help="contact")
    move_id = fields.Many2one("op.ticket", string="Dummy", help="contact")
    user_id = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        vals['tockens'] = self.env['ir.sequence'].next_by_code('appointment.menu')
        return super(AppointmentMenu, self).create(vals)

    def confirm_action(self):
        self.state = "appointment"

    def convert_action(self):
        self.state = "op"
        move_vals = {
            'patient_card_id': self.patientcard_id.id,
            'name_id': self.patientname,
            'doctor_id': self.doctorname_id.id,
            'date': self.datei,
        }
        move_id = self.env['op.ticket'].create(move_vals)
        self.move_id = move_id.id
        return True

    def action_open_op(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'op',
            'res_model': 'op.ticket',
            'view_mode': 'form',
            'res_id': self.move_id.id,
            'target': 'current'
        }
