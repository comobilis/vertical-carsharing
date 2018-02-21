# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class VehicleDestCost(models.Model):
    _name = "vehicle.dest.cost"

    from_dist = fields.Integer(
        string="From (KM)",
        required=True,
    )
    to_dist = fields.Integer(
        string="To (KM)",
        required=True,
    )
    price_km = fields.Float(
        string="Cost / KM",
        required=True,
    )
    fleet_vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string="Fleet Vehicle",
    )
    
class VehicleTimeCost(models.Model):
    _name = "vehicle.time.cost"

    from_hour = fields.Integer(
        string="From (HR)",
        required=True,
    )
    to_hour = fields.Integer(
        string="To (HR)",
        required=True,
    )
    price_hour = fields.Float(
        string="Cost / HR",
        required=True,
    )
    fleet_vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string="Fleet Vehicle",
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
