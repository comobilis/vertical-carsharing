# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class FleetVehicleSubType(models.Model):
    _name = "fleet.vehicle.sub.type"

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
    )

    @api.multi
    def action_show_vehicles(self):
        for rec in self:
            vehicle_ids = rec.env['fleet.vehicle'].search([
                ('vehicle_sub_type_id', '=', rec.id)])
            action = rec.env.ref('fleet.fleet_vehicle_action').read()[0]
            action['domain'] = [('id', 'in', vehicle_ids.ids)]
            return action
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
