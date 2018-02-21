# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MembershipDeposit(models.Model):
    _name = "membership.deposit"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Membership Deposit"
    _order = 'id desc'

    name = fields.Char(
        string="Name",
        default='New',
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    create_user_id = fields.Many2one(
        "res.users",
        string="Created by",
        readonly=True,
        default=lambda self:self.env.user.id,
    )
    create_date = fields.Datetime(
        string="Create Date",
        readonly=True,
        default=fields.Datetime.now()
    )
    deposit_amount = fields.Float(
        string="Deposit Amount",
        required=True,
    )
    rfid_code = fields.Char(
        string="RFID Key",
        copy=False,
    )
    note = fields.Text(
        string="Text",
    )
    product_id = fields.Many2one(
        'product.product',
        string="Product",
#        required=True,
    )
    confirm_user_id = fields.Many2one(
        'res.users',
        string="Confirm By",
        readonly=True,
    )
    confirm_datetime = fields.Datetime(
        string="Confirm Date",
        readonly=True,
    )
    approve_user_id = fields.Many2one(
        'res.users',
        string="Approve By",
        readonly=True,
    )
    approve_datetime = fields.Datetime(
        string="Approve Date",
        readonly=True,
    )
    state = fields.Selection(
        selection=[
                   ('draft','Draft'),
                   ('confirm','Confirmed'),
                   ('approved','Approved'),
                   ('cancel','Cancel'),
                   ('invoice_created','Invoice Created'),
                   ('rfid_generated','RFID Key Generated'),
                   ('reject','Reject')
        ],
        string="Status",
        default='draft',
        track_visibility='onchange',
    )
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self:self.env.user.company_id,
        readonly=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self:self.env.user.company_id.currency_id,
    )
    invoice_ids = fields.One2many(
        'account.invoice',
        'membership_deposit_id',
        string="Invoices",
        readonly=True,
        store=True,
    )
    is_cancel_invoice = fields.Boolean(
        string="Is Cancel Invoice",
        compute="_compute_cancel_invoice",
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
    )
    payment_level_id = fields.Many2one(
        'membership.payment.level',
#        required=True,
        string="Membership Level",
    )
    
    def _pass_membership_level(self, deposit_id=None,vals=None):
        if deposit_id and deposit_id.employee_id and deposit_id.employee_id.user_id and deposit_id.employee_id.user_id.partner_id:
            if vals != None:
                deposit_id.employee_id.payment_level_id = vals.get('payment_level_id')
                deposit_id.employee_id.user_id.payment_level_id = vals.get('payment_level_id')
                deposit_id.employee_id.user_id.partner_id.payment_level_id = vals.get('payment_level_id')
            else:
                deposit_id.employee_id.payment_level_id = deposit_id.payment_level_id.id
                deposit_id.employee_id.user_id.payment_level_id = deposit_id.payment_level_id.id
                deposit_id.employee_id.user_id.partner_id.payment_level_id = deposit_id.payment_level_id.id
        return True
        
    @api.depends("invoice_ids","invoice_ids.state")
    def _compute_cancel_invoice(self):
        if any([not x.state == 'cancel' for x in self.invoice_ids]) and self.state == "invoice_created":
            self.is_cancel_invoice = False
        elif any([x.state == 'cancel' for x in self.invoice_ids]):
            self.is_cancel_invoice = True

    @api.multi
    def unlink(self):
        for rec in self:
            if not rec.state == 'draft':
                raise ValidationError("You can not delete record until is not in draft state")
            else:
                return super(MembershipDeposit,self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            if vals.get('name', 'New') != 'New':
                vals['name'] = 'New'

        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence']\
                .next_by_code('membership.deposit') or 'New'
        result = super(MembershipDeposit, self).create(vals)
        self._pass_membership_level(result)
        return result
        
    @api.multi
    def write(self, vals):
        for rec in self:
            if vals.get('payment_level_id'):
                self._pass_membership_level(rec,vals)
        return super(MembershipDeposit, self).write(vals)

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            rec.confirm_user_id = rec.env.user.id
            rec.confirm_datetime = fields.Datetime.now()
            
    @api.multi
    def action_approved(self):
        for rec in self:
            rec.state = 'approved'
            rec.approve_user_id = rec.env.user.id
            rec.approve_datetime = fields.Datetime.now()
    
    @api.multi
    def action_create_invoice(self):
        invoice_obj = self.env['account.invoice']
        invoice_line_obj = self.env['account.invoice.line']
        for rec in self:
            account_id = False
            if rec.product_id:
                account_id = rec.product_id.property_account_income_id or\
                    rec.product_id.categ_id.property_account_income_categ_id
                line_vals = {
                    'product_id': rec.product_id.id,
                }
            else:
                raise ValidationError("Please Select One product")

            if not account_id:
                raise ValidationError("No anyone account Found")

            new_line = invoice_line_obj.new({'product_id': rec.product_id.id})
            new_line._onchange_product_id()
            
#            taxes_id = schedule.vehicle_id.product_id.taxes_id
#            fpos = schedule.partner_id.property_account_position_id
#            if fpos:
#                taxes_id = fpos.map_tax(schedule.vehicle_id.product_id.taxes_id, schedule.vehicle_id.product_id, schedule.partner_id)

            line_vals.update({
                'name': rec.name + " - "+str(rec.deposit_amount)+" of " + rec.partner_id.name,
                'quantity': 1,
#                'invoice_line_tax_ids':[(6, 0, taxes_id.ids)],
                'price_unit': rec.deposit_amount,
                'account_id': account_id.id,
#                'vehicle_id': schedule.vehicle_id.id,
#                'reservation_schedule_id': schedule.id,
            })
            line_ids = invoice_line_obj.create(line_vals)

            default_fields = [
                'user_id',
                'journal_id',
                'company_id',
            ]
            invoice_vals = invoice_obj.default_get(default_fields)
            invoice_vals.update({
                'partner_id': rec.partner_id.id,
                'currency_id':rec.currency_id.id,
                'date_invoice': fields.Datetime.now(),
                'invoice_line_ids': [(6, 0, line_ids.ids)],
#                'reservation_employee_id': rec.reserving_employee_id.id,
#                'vehicle_reservation_id': rec.id,
#                'is_reservation_invoice': True,
            })
            invoice = invoice_obj.new(invoice_vals)
            invoice._onchange_partner_id()
            invoice_vals.update({'account_id': invoice.account_id.id,
                                 'comment': rec.note})
            invoice_id = invoice_obj.create(invoice_vals)
            rec.invoice_ids += invoice_id

            rec.state = 'invoice_created'
    
    @api.multi
    def action_generate_rfid(self):
        for rec in self:
            if rec.employee_id and rec.rfid_code:
                rec.employee_id.rfid_key = rec.rfid_code
                rec.state = 'rfid_generated'
            else:
                raise ValidationError("Please Select Employee or RFID Key")
            return rec
            
    @api.multi
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
            
    @api.multi
    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'
            
    @api.multi
    def action_reject(self):
        for rec in self:
            rec.state = 'reject'
    
    @api.multi
    def action_invoice(self):
        invoice = self.mapped('invoice_ids')
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['domain'] = [('id', 'in', invoice.ids)]
        return action


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
