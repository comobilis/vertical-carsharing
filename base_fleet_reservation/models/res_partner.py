# -*- coding: utf-8 -*-

#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    department_id = fields.Many2one(
        'hr.department',
        string="Department",
    )

    @api.multi
    def action_vehicle_reservation(self):
        for rec in self:
            reservation_ids = rec.env['fleet.vehicle.reservation'].search([('partner_id', '=' ,rec.id)])
            action = rec.env.ref("base_fleet_reservation.action_fleet_vehicle_reservation").read()[0]
            action['domain'] = [('id', 'in', reservation_ids.ids)]
            return action


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
