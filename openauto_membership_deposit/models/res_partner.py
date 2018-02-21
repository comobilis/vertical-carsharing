# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.


from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    payment_level_id = fields.Many2one(
        'membership.payment.level',
#        required=True,
        string="Membership Level",
    )
    rfid_key = fields.Char(
        string="RFID Key",
        copy=False,
        readonly=True,
        store=True,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
