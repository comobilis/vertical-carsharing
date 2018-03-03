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
        print ("&&&&&&&&&&&&&&&&&&",self)
#        active_ids = self._context.get('active_ids')
#        print ("+====================",active_ids)
#        for rec in self:
#            if rec.employee_ids:
#                for employee in rec.employee_ids:
#                    event_ids = event_obj.search([('vehicle_reserved_employee_id','in',rec.employee_ids.ids),('start','>=',rec.start_date),('stop','<=',rec.end_date)])
#                print ("-----------------------------",event_ids)

        data = self.read()[0]
        return self.env.ref('openauto_report.report_vehicle_bookings').report_action(self.ids, data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
