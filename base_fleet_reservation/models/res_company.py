# -*- coding: utf-8 -*-

#See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    advance_payment = fields.Boolean(
        string="Do Advance Payment",
    )
    advance_payment_option = fields.Selection(
        selection=[('period_amount', 'Is it billed monthly or yearly'),
                   ('entity_amount', 'Is it billed per employee or Unit'),
                   ('levels', 'Different Levels')],
        string="Advance Payment Option",
    )
    advance_payment_level_ids = fields.One2many(
        'advance.payment.level',
        'company_id',
        string="Payment Level"
    )
    coordinator_user_id = fields.Many2one(
        'res.users',
        string="Coordinator",
    )
    reserved_the_day_of_use = fields.Integer(
        string="Reserved the Day of use (Last Minute)",
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
