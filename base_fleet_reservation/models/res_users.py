# -*- coding: utf-8 -*-

#See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"
    
    department_id = fields.Many2one(
        'hr.department',
        string="Department",
    )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
