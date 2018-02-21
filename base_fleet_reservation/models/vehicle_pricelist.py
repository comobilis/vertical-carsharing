# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class VehiclePricelist(models.Model):
    _name = "vehicle.pricelist"

    name = fields.Char(
        string="Name",
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
    )
    vehicle_pricelist_line_ids = fields.One2many(
        "vechicle.pricelist.line",
        "pricelist_id",
        string="Pricelist Line",
    )


class VechiclePricelistLine(models.Model):
    _name = "vechicle.pricelist.line"

    pricelist_type = fields.Selection(
        selection=[('days', 'Day'),
                   ('hours', 'Hours'),
                   ('both', 'Both'), ],
        default="days",
        string="Type",
        required=True,
    )
    day = fields.Selection(
        selection=[('0', 'Sunday'),
                   ('1', 'Monday'),
                   ('2', 'Tuesday'),
                   ('3', 'Wednesday'),
                   ('4', 'Thursday'),
                   ('5', 'Friday'),
                   ('6', 'Saturday'), ],
        defualt='0',
        string="Day",
    )
    start_time = fields.Float(
        string="Start Time",
    )
    end_time = fields.Float(
        string="End Time",
    )
    percentage = fields.Float(
        string="Percentage",
        required=True,
        help="Enter Percentage to set price",
    )
    pricelist_id = fields.Many2one(
        'vehicle.pricelist',
        string="Pricelist",
    )
    start_date = fields.Date(
        string="Start Date",
    )
    end_date = fields.Date(
        string="End Date",
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
