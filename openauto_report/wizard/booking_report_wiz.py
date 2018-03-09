# -*- coding: utf-8 -*-

# Part of Openauto.
#See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookingReportWiz(models.TransientModel):
    _name = "booking.report.wiz"
    
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string="Department",
        required=True,
    )
    employee_ids = fields.Many2many(
        'hr.employee',
        string="Employee",
    )
    start_date = fields.Date(
        string="Start Date",
        required=True,
        default=datetime.strptime(fields.Datetime.now(),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-01'),
    )
    end_date = fields.Date(
        string="End Date",
        required=True,
        default=str(datetime.strptime(fields.Datetime.now(),'%Y-%m-%d %H:%M:%S') + relativedelta(months=+1, day=1, days=-1))[:10]
    )
    
    @api.multi
    def action_print_report(self):
        event_obj = self.env['calendar.event']
        data = self.read()[0]
        return self.env.ref('openauto_report.report_vehicle_bookings').report_action(self.ids, data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
