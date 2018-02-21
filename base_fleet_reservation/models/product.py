# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Product(models.Model):
    _inherit = "product.product"

    is_vehicle = fields.Boolean(
        string='Is Vehicle Product',
    )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
