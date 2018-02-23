# -*- coding: utf-8 -*-

#See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class AdvancePaymentLevel(models.Model):
    _name = "advance.payment.level"
    _rec_name = "payment_level_id"

#    payment_level = fields.Selection(
#        selection=[('level1', 'Level 1'),
#                   ('level2', 'Level 2'),
#                   ('level3', 'Level 3'),
#                   ('level4', 'Level 4'),
#                   ('level5', 'Level 5')],
#        string="Payment Level",
#        required=True,
#    )
    payment_level_id = fields.Many2one(
        'membership.payment.level',
        required=True,
        string="Payment Level",
    )
    amount = fields.Float(
        string="Amount",
        required=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string="Company",
    )

    _sql_constraints = [
        ('Level_company_uniq', 'unique (payment_level_id, company_id)',
            'The code of the account must be unique per company !')
    ]


class MembershipPaymentLevel(models.Model):
    _name = "membership.payment.level"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
