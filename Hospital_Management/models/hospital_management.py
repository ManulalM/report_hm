from datetime import date
from odoo import api, fields,  models


class HospitalManagement(models.Model):
    _name = "hospital.management"
    _inherit = ["mail.thread"]
    _description = "This model contains the details of hospital management system"
    _rec_name = "name_id"

    patient_id = fields.Char(String='PID', help="contact")
    name_id = fields.Many2one('res.partner', string="Name", help="contact")
    dob = fields.Date(String="Date of Birth", related='name_id.dob', help="contact")
    age = fields.Integer(string="Age", compute='calculate_age', help="contact")
    address = fields.Text(String="Address", help="contact")
    contact = fields.Char(string="Mobile", related='name_id.mobile', help="contact")
    gender = fields.Selection(String='Gender', related='name_id.gender', help="contact")
    blood_group = fields.Selection([('a+ve', 'A+ve'), ('b+ve', 'B+ve'), ('o+ve', 'O+ve')], help="contact")
    note = fields.Text(string='Description', help="contact")
    medicine_ids = fields.One2many("op.ticket", "patient_card_id", string="local")


    @api.onchange('name_id')
    def _onchange_name(self):
        print("name_id", self.name_id.ids)

        if self.name_id:
            self.address = self.name_id.street
        else:
            self.address = False

    @api.model
    def create(self, vals):
        vals['patient_id'] = self.env['ir.sequence'].next_by_code('hospital.management')
        return super(HospitalManagement, self).create(vals)

    @api.depends('dob')
    def calculate_age(self):
        for i in self:
            today = date.today()
            if i.dob:
                i.age = today.year - i.dob.year
            else:
                i.age = 0
