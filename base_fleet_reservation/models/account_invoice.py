# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

import datetime
import calendar
from odoo import models, fields, api
from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    vehicle_reservation_id = fields.Many2one(
        'fleet.vehicle.reservation',
        string="Vehicle Reservation",
        readonly=True,
    )
    reservation_employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        readonly=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
    )
    is_reservation_invoice = fields.Boolean(
        string="Is Vehicle Reservation Invoice ?",
        readonly=True,
    )
    reservation_schedule_id = fields.Many2one(
        'vehicle.reservation.schedule',
        string="Reservation Schedule",
    )

    @api.model
    def _cron_send_mail(self):
        date = datetime.datetime.now()
        start_date = date.replace(day=1)
        end_date = date.replace(day=calendar.monthrange(
                                date.year,
                                date.month)[1])

        invoice_ids = self.search([('type', '=', 'out_invoice'),
                                   ('state', 'not in',
                                    ['draft', 'paid', 'cancel']),
                                   ('date_invoice', '>=', start_date),
                                   ('date_invoice', '<=', end_date)])

        for invoice in invoice_ids:
            email_template = self.env.ref('account.email_template_edi_invoice')
            email_template.send_mail(invoice.id, force_send=True)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    reservation_schedule_id = fields.Many2one(
        'vehicle.reservation.schedule',
        string="Reservation Schedule",
    )
    vehicle_type_id = fields.Many2one(
        'fleet.vehicle.type',
        string="Vehicle Type",
    )
    vehicle_sub_type_id = fields.Many2one(
        'fleet.vehicle.sub.type',
        string="Vehicle Sub Type",
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string="Vehicle",
    )
#    start_date_time = fields.Datetime(
#        string="Start Date",
#        required=True,
#    )
#    end_date_time = fields.Datetime(
#        string="End Date",
#        required=True,
#    )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
