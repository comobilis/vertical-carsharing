# -*- coding: utf-8 -*-

#See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    charge_deposit = fields.Boolean(
        string="Is Charge Deposit",
        help="Add Deposit to the vehicle",
    )
#    deposit_charge_amount = fields.Float(
#        string="Deposit Amount"
#    )
    yearly_employee_fee = fields.Boolean(
        string="Yearly Fee Per Employee",
    )
    yearly_employee_fee_amt = fields.Float(
        string="Yearly Fee Amount Per Employee",
    )
    yearly_unit_fee = fields.Boolean(
        string="Yearly Fee Per Unit",
    )
    yearly_unit_fee_amt = fields.Float(
        string="Yearly Fee Amount Per Unit",
    )
    advance_payment = fields.Boolean(
        string="Do Advance Payment",
    )
    advance_payment_option = fields.Selection(
        selection=[('period_amount', 'Is it billed monthly or yearly'),
                   ('entity_amount', 'Is it billed per employee or Unit'),
                   ('levels', 'Different Levels')],
        string="Advance Payment Option",
    )
#    advance_payment_level_ids = fields.One2many(
#        'advance.payment.level',
#        'company_id',
#        string="Payment Level"
#    )

    #Vehicle Reservation Information
    max_vehicle_perunit = fields.Integer(
        string='Max Vehicle Per Unit',
        copy=True,
    )
#    is_car_taken = fields.Boolean(
#        string='Is Car Taken ?',
#        copy=True,
#    )
    car_taken_minute = fields.Float(
        string='Grace Checkin.period',
        copy=True,
    )
#    is_reservation_block = fields.Boolean(
#        string='Is Reservation Block ?',
#        copy=True,
#    )
    reserve_block_days = fields.Float(
        string='Grace Invoice.period',
        copy=True,
        help="Block Days for open invoices",
    )
    allow_external_user = fields.Boolean(
        string='Is Allow External User ?',
        copy=True,
    )
    employee_present_status = fields.Selection([
        ('present', 'Employee/Member Present'),
        ('absent', 'Employee/Member Not Present')]
    )
#    is_employee_link = fields.Boolean(
#        string='Is Employee Link ?',
#        copy=True,
#    )
#    is_employee_unlink = fields.Boolean(
#        string='Is Employee UnLink ?',
#        copy=True,
#    )
    person_phone = fields.Char(
        string='Person Phone',
        copy=True,
    )
    person_name = fields.Char(
        string="Person Name",
    )
    invoice_amount = fields.Float(
        string="Invoice Amount.min",
        help="Minimum Invoice Amount",
    )
    allow_minimum_month_invoice = fields.Integer(
        string="Allowed Minimum Month",
        help="MInimum Month to Create invoice",
        default=3,
    )
    reimbursement_of_expenses = fields.Float(
        string="Reimbursement Amount.min",
    )
    minimum_billing_reserve_time = fields.Float(
        string="Minimum billing for the Reserved Time"
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
