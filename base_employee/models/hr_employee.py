# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    rfid_number = fields.Char(
        string="RFID",
        copy=False,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
