# -*- coding: utf-8 -*-

# Part of Openauto.
#See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OpenautoBookingReport(models.AbstractModel):
    _name = 'report.openauto_report.vehicle_bookings_report'

    @api.model
    def get_report_values(self, docids, data=None):
        print ("^^^^^^^^^^^^^^^^^^^",data)
        active_ids = data['context'].get('active_ids')
        print ('---------------',active_ids,)
        booking_wizard_obj = self.env['booking.report.wiz']
        booking_wizard_ids = booking_wizard_obj.browse(active_ids)
        event_obj = self.env['calendar.event']
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if data.get('employee_ids'):
            employee_ids = data.get('employee_ids')
        else:
            department = self.env['hr.department'].browse(data.get('department_id')[0])
            print ("**************",department)
            employee_ids = department.member_ids.ids
            print ("--------------------",employee_ids)
        booking_dict = {}
        user_ids = []
        for employee in employee_ids:
            employee_id = self.env['hr.employee'].browse(employee)
            event_ids = event_obj.search([('vehicle_reserved_employee_id','=',employee),('start','>=',start_date),('start','<=',end_date)])
            if event_ids:
                booking_dict.update({employee_id : event_ids})
        bookig_report = self.env['ir.actions.report']._get_report_from_name('openauto_report.vehicle_bookings_report')
        booking_report_dict = {
            'start_date': start_date,
            'end_date': end_date,
        }
        if data.get(booking_wizard_ids,False):
            user_ids = [booking_wizard_ids][0]
        else:
            user_ids = docids
        print ("&&&&&&&&&&&&&&&&&&&&&",booking_wizard_ids,user_ids)
        return {
                    'doc_ids': user_ids,
                    'doc_model': 'booking.report.wiz',
                    'docs': booking_wizard_ids,
                    'doc_report':booking_report_dict,
                    'bookings':booking_dict,
                }
