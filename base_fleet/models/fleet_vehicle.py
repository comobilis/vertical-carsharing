# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    vehicle_type_id = fields.Many2one(
        'fleet.vehicle.type',
        string='Vehicle Type'
    )
    vehicle_sub_type_id = fields.Many2one(
        'fleet.vehicle.sub.type',
        string='Vehicle Sub Type'
    )
    is_reservable = fields.Boolean(
        string='Is Reservable',
    )
    reserve_period = fields.Selection(
        selection=[('always', 'Always'),
                   ('some_time', 'For Some Time Available'),
                   ('not_avail', 'For Some Time Not Available')],
        default='always',
    )
    available_from = fields.Float(
        string="Available From",
    )
    available_to = fields.Float(
        string="Available To",
    )
    not_available_from = fields.Float(
        string="Not Available From",
    )
    not_available_to = fields.Float(
        string="Not Available To",
    )
    is_use_vehicle_fees = fields.Boolean(
        string="Is Use Vehicle Fees",
    )
    vehicle_dest_cost_ids = fields.One2many(
        'vehicle.dest.cost',
        'fleet_vehicle_id',
        string="Vehicle Destination Cost",
    )
    is_use_vehicle_time_fees = fields.Boolean(
        string="Is Use Vehicle Hourly Fees",
    )
    vehicle_time_cost_ids = fields.One2many(
        'vehicle.time.cost',
        'fleet_vehicle_id',
        string="Vehicle Hourly Cost",
    )
    vehicle_reserve_time = fields.Selection([
        ('each_day', 'Reserved Each Day'),
        ('each_hour_on_days', 'For Each Hour During Hour on Day(s)'),
        ('day_per_hour_x', 'For Each Hour During Day/Hour'),
        ('day_per_hour_y', 'For Each Hour During Day/hour'),
        ('allow_higher_pricing', 'Allow Higher Pricing')],
        default="each_day",
        string='Vehicle Reserve Time'
    )
    during_hour_from = fields.Float(
        string="Hour During From",
    )
    during_hour_to = fields.Float(
        string="Hour During To",
    )
    during_per_hour_from = fields.Float(
        string="During Per Hour From",
    )
    during_per_hour_to = fields.Float(
        string="During Per Hour To",
    )
    allow_higher_pricing = fields.Float(
        string="Allow Higher Pricing",
        help="Allow Higher Pricing for Weekends,\
        Lower for Weekdays, Lower for other Hours",
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
