# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class FleetVehicleReservation(models.Model):
    _inherit = "fleet.vehicle.reservation"

    @api.multi
    def action_confirm(self):
        for rec in self:
            res = super(FleetVehicleReservation,self).action_confirm()
            state_labels = dict(self.fields_get(['state'])['state']['selection'])
            email_template = self.env.ref('vehicle_reservation_notification.email_template_reservation_confirm')
            email_template.with_context(state_labels).send_mail(rec.id, force_send=True)
        return rec
    
    @api.multi
    def action_approve_hod(self):
        for rec in self:
            res = super(FleetVehicleReservation,self).action_approve_hod()
            state_labels = dict(self.fields_get(['state'])['state']['selection'])
            email_template = self.env.ref('vehicle_reservation_notification.email_template_reservation_hou_approv')
            email_template.with_context(state_labels).send_mail(rec.id, force_send=True)
        return rec
    
    @api.multi
    def action_approve_offi(self):
        for rec in self:
            res = super(FleetVehicleReservation,self).action_approve_offi()
            state_labels = dict(self.fields_get(['state'])['state']['selection'])
            email_template = self.env.ref('vehicle_reservation_notification.email_template_reservation_coordinator_approv')
            email_template.with_context(state_labels).send_mail(rec.id, force_send=True)
        return rec
        
    @api.multi
    def action_reserve(self):
        for rec in self:
            res = super(FleetVehicleReservation,self).action_reserve()
            state_labels = dict(self.fields_get(['state'])['state']['selection'])
            email_template = self.env.ref('vehicle_reservation_notification.email_template_reservation_manager_approv')
            email_template.with_context(state_labels).send_mail(rec.id, force_send=True)
        return rec
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
