# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

import pytz
import datetime
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import ValidationError


class FleetVehicleReservation(models.Model):
    _name = "fleet.vehicle.reservation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Vehicle Reservation"
    _order = 'id desc'

    name = fields.Char(
        string="Number",
        default='New',
        copy=False,
        readonly=True,
    )
    reservation_schedule_ids = fields.One2many(
        'vehicle.reservation.schedule',
        'fleet_vehicle_reservation_id',
        string="Reservation Schedule",
    )
    reserving_employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        required=True,
    )
    rfid_key = fields.Char(
        string="RFID Key",
#        readonly=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.user.company_id,
        string="Company",
        readonly=True,
    )
    state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('confirm', 'Waiting for HOU Approval'),
                   ('approve_hod', 'Approved By HOU'),
                   ('approve_offi', 'Approved By Coordinator'),
                   ('reserved', 'Reserved'),
                   ('invoice', 'Invoice Created'),
                   ('paid', 'Paid'),
                   ('reject', 'Rejected'),
                   ('cancel', 'Cancel')],
        default="draft",
        string="State",
        track_visibility='onchange',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        required=True,
    )
    calendar_event_ids = fields.One2many(
        'calendar.event',
        'vehicle_reservation_id',
        string="Reservation Events",
    )
    is_ride_share = fields.Boolean(
        string="I’m willing to Rideshare",
    )
    rides_msg = fields.Char(
        string="Ride Message",
        default="I’m going to",
    )
    phone_number = fields.Char(
        string="Phone",
    )
    is_service_vehicle_reservation = fields.Boolean(
        string="This reservation is to be able to Service the vehicle",
    )
    reservation_service_type_id = fields.Many2one(
        'fleet.service.type',
        string="Service Type",
    )
    acount_invoice_ids = fields.One2many(
        'account.invoice',
        'vehicle_reservation_id',
        string='Invoice',
    )
    create_date = fields.Date(
        string="Create Date",
        default=fields.Datetime.now,
        readonly=True,
    )
    created_user_id = fields.Many2one(
        'res.users',
        string="Created By",
        default=lambda self: self.env.user.id,
        readonly=True,
    )
    refernce = fields.Char(
        string="Reference",
    )
    note = fields.Text(
        string="Notes",
    )
    is_reserve_for_other = fields.Boolean(
        string="This reservation is for Friends or Family",
    )
    employee_present_status = fields.Selection([
        ('present', 'Employee/Member Present'),
        ('absent', 'Employee/Member Not Present')],
        string="Is for Other User?",
    )
    person_phone = fields.Char(
        string='Person Phone',
        copy=True,
    )
    person_name = fields.Char(
        string="Person Name",
    )
    invoice_amount = fields.Float(
        string="Invoice Amount.min",
    )
    pricelist_id = fields.Many2one(
        'vehicle.pricelist',
        string="Pricelist",
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        default=lambda self: self.env.user.company_id.currency_id,
    )
    is_cancel_invoice = fields.Boolean(
        string="Is Cancel Invoice",
        compute="_compute_cancel_invoice",
    )
    hou_user_id = fields.Many2one(
        'res.users',
        string="Head of Unit",
    )
    hou_approved_date_time = fields.Datetime(
        string="Head of Unit Approval Date",
        readonly=True,
    )
    coordinator_user_id = fields.Many2one(
        'res.users',
        string="Coordinator",
    )
    coordinator_approved_date_time = fields.Datetime(
        string="Coordinator Approval Date",
        readonly=True,
    )
    manager_user_id = fields.Many2one(
        'res.users',
        string="Manager",
    )
    manager_approved_date_time = fields.Datetime(
        string="Manager Approval Date",
        readonly=True,
    )
    invoice_partner_id = fields.Many2one(
        'res.partner',
        string="Invoice Partner",
    )

    @api.depends("reservation_schedule_ids","reservation_schedule_ids.invoice_id","reservation_schedule_ids.invoice_id.state")
    def _compute_cancel_invoice(self):
        if any([not x.invoice_id for x in self.reservation_schedule_ids]) and self.state == "reserved":
            self.is_cancel_invoice = True
        elif any([x.invoice_id.state == 'cancel' for x in self.reservation_schedule_ids]):
            self.is_cancel_invoice = True
#        if all([x.invoice_id.state == 'paid' for x in self.reservation_schedule_ids]):
#            self.state = 'paid'

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        if self.pricelist_id:
            self.currency_id = self.pricelist_id.currency_id.id

    @api.onchange('reserving_employee_id', 'company_id')
    def _onchange_employee_id(self):
        self.partner_id = self.reserving_employee_id.address_home_id.id
        self.department_id = self.reserving_employee_id.department_id.id
        self.hou_user_id = self.reserving_employee_id.department_id.hou_user_id.id
        self.coordinator_user_id = self.company_id.coordinator_user_id.id
        self.rfid_key = self.reserving_employee_id.rfid_key
        
    @api.onchange('hou_user_id')
    def _onchange_hou_user_id(self):
        self.invoice_partner_id = self.hou_user_id.partner_id.id

#    @api.onchange('is_reserve_for_other')
#    def _onchange_is_reserve_for_other(self):
#        for schedule_id in self.reservation_schedule_ids:
#            if not schedule_id.vehicle_id.is_allowed_friend_family and self.is_reserve_for_other:
#                self.is_reserve_for_other = False
#                raise ValidationError("%s Vehicle is not allowed for others."%(schedule_id.vehicle_id.name))

    def _check_max_vehicle_per_unit(self):
        for schedule_id in self.sudo().reservation_schedule_ids:
            vehicle_on_unit = self.env['calendar.event'].search_count([('start','=',schedule_id.start_date_time),('stop','=',schedule_id.end_date_time),('department_id','=',schedule_id.department_id.id)])
            if (vehicle_on_unit > 0) and (vehicle_on_unit >= schedule_id.department_id.max_vehicle_perunit and schedule_id.department_id.max_vehicle_perunit > 0):
                raise ValidationError("You have reached on reservation Limit of this Unit")
            elif (vehicle_on_unit > 0) and (schedule_id.department_id.max_vehicle_perunit == 0) and (vehicle_on_unit >= schedule_id.department_id.company_id.max_vehicle_perunit and schedule_id.department_id.company_id.max_vehicle_perunit > 0):
                raise ValidationError("You have reached on reservation Limit of this Unit")
        return True

    def _check_reserved_vehicle(self):
        for schedule_id in self.sudo().reservation_schedule_ids:
            start_date = datetime.datetime.strptime(
                schedule_id.start_date_time,
                '%Y-%m-%d %H:%M:%S'
            )
            timezone = pytz.timezone(self._context.get('tz') or 'UTC')
            end_date = datetime.datetime.strptime(
                schedule_id.end_date_time,
                '%Y-%m-%d %H:%M:%S'
            )
            if end_date < start_date:
                raise ValidationError(_(
                    'Ending datetime cannot be set before starting datetime.'
                ))
            if schedule_id.vehicle_id.reserve_period == 'some_time':
                avail_from = '{0:02.0f}:{1:02.0f}'.\
                    format(*divmod(
                        schedule_id.vehicle_id.available_from * 60,
                        60))
                avail_to = '{0:02.0f}:{1:02.0f}'.\
                    format(*divmod(
                        schedule_id.vehicle_id.available_to * 60,
                        60))

                tzone_start_date = pytz.UTC.localize(start_date)
                start_date_tz = tzone_start_date.astimezone(timezone)

                tzone_end_date = pytz.UTC.localize(end_date)
                end_date_tz = tzone_end_date.astimezone(timezone)
                
#                start_hrs_tz = float(start_date.hour) +\
#                    (float(start_date_tz.minute) / 60)
#                end_hrs_tz = float(end_date.hour) +\
#                    (float(end_date_tz.minute) / 60)
#                    

                if not (str(start_date_tz.time()) >= str(avail_from) and
                        str(start_date_tz.time()) <= str(avail_to)):
                    raise ValidationError(_("This vehicle is available\
                                for %s to %s." % (avail_from, avail_to)))

                elif not (str(end_date_tz.time()) >= str(avail_from) and
                          str(end_date_tz.time()) <= str(avail_to)):
                    raise ValidationError(_("This vehicle is available\
                                for %s to %s." % (avail_from, avail_to)))

            elif schedule_id.vehicle_id.reserve_period == 'not_avail':
                avail_from = '{0:02.0f}:{1:02.0f}'.\
                    format(*divmod(
                        schedule_id.vehicle_id.not_available_from * 60,
                        60))
                avail_to = '{0:02.0f}:{1:02.0f}'.\
                    format(*divmod(
                        schedule_id.vehicle_id.not_available_to * 60,
                        60))

                tzone_start_date = pytz.UTC.localize(start_date)
                start_date_tz = tzone_start_date.astimezone(timezone)

                tzone_end_date = pytz.UTC.localize(end_date)
                end_date_tz = tzone_end_date.astimezone(timezone)
                
#                start_hrs_tz = float(start_date_tz.hour) +\
#                    (float(start_date_tz.minute) / 60)
#                end_hrs_tz = float(end_date_tz.hour) +\
#                    (float(end_date_tz.minute) / 60)
#                    

                if str(start_date_tz.time()) >= str(avail_from) and\
                        str(start_date_tz.time()) <= str(avail_to):
                    raise ValidationError(_("This vehicle is not available\
                                for %s to %s." % (avail_from, avail_to)))
                elif str(end_date_tz.time()) >= str(avail_from) and\
                        str(end_date_tz.time()) <= str(avail_to):
                    raise ValidationError(_("This vehicle is not available\
                                for %s to %s." % (avail_from, avail_to)))

            event_ids = self.env['calendar.event'].search(
                [('vehicle_id', '=', schedule_id.vehicle_id.id)]
            )
            for event in event_ids:
                if event.start_datetime >= schedule_id.start_date_time and\
                        event.start_datetime <= schedule_id.end_date_time:
                    raise ValidationError(_("This vehicle is already reserved\
                                             on your selected date."))
                elif event.stop_datetime >= schedule_id.start_date_time and\
                        event.stop_datetime <= schedule_id.end_date_time:
                    raise ValidationError(_("This vehicle is already reserved\
                                             on your selected date."))
        return True

    def _is_partner_block(self, rec):
        invoice_obj = rec.env['account.invoice']
        invoice_ids = invoice_obj.sudo().search([
            ('partner_id', '=', rec.invoice_partner_id.id),
            ('state', '=', 'open')]
        )
        if not invoice_ids:
            return False
        due_date = False
        for invoice in invoice_ids:
            if not due_date:
                due_date = invoice.date_due
            elif due_date and\
                    due_date > invoice.date_due:
                    due_date = invoice.date_due
        if due_date:
            date_due = datetime.datetime.strptime(
                due_date, DEFAULT_SERVER_DATE_FORMAT
            )
            block_date = date_due +\
                timedelta(days = self.company_id.reserve_block_days)
            if str(block_date) <= fields.Datetime.now():
                raise ValidationError(_("You were block please pay last\
                    invoice")
                )
        return False
    
    
    @api.model
    def create(self, vals):
        if vals.get("is_reserve_for_other"):
            for schedule_id in self.reservation_schedule_ids:
                if not schedule_id.vehicle_id.is_allowed_friend_family:
                    raise ValidationError("%s Vehicle is not allowed for others."%(schedule_id.vehicle_id.name))
#        if vals.get('reserving_employee_id'):
#            employee_id = self.env['hr.employee'].browse(int
#                (vals.get('reserving_employee_id'))
#            )
#            company_id = self.env.user.company_id
#            if employee_id.open_invoice_due_date:
#                due_date = datetime.datetime.strptime(
#                    employee_id.open_invoice_due_date,"%Y-%m-%d %H:%M:%S"
#                )
#                block_date = due_date +\
#                    timedelta(days=company_id.reserve_block_days)
#                if str(block_date) <= fields.Datetime.now():
#                    raise ValidationError(_("You were block please pay last\
#                        invoice")
#                    )
        if vals.get('name', False):
            if vals.get('name', 'New') != 'New':
                vals['name'] = 'New'

        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence']\
                .next_by_code('fleet.vehicle.reservation') or 'New'
        result = super(FleetVehicleReservation, self).create(vals)
        result._check_reserved_vehicle()
        return result

    @api.multi
    def write(self, vals):
        result = super(FleetVehicleReservation, self).write(vals)
        if self.is_reserve_for_other:
            for schedule_id in self.reservation_schedule_ids:
                if not schedule_id.vehicle_id.is_allowed_friend_family:
                    raise ValidationError("%s Vehicle is not allowed for others."%(schedule_id.vehicle_id.name))
        for rec in self:
            if 'reservation_schedule_ids' in vals:
                rec._check_reserved_vehicle()
        return result

    @api.multi
    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec._check_max_vehicle_per_unit()
            rec._check_reserved_vehicle()
            block = rec._is_partner_block(rec)
            if rec.hou_user_id and not block:
                rec.state = 'confirm'
            else:
                raise ValidationError("Please Select Your Head of Unit")

    @api.multi
    def action_approve_hod(self):
        for rec in self:
            rec._check_reserved_vehicle()
            if rec.hou_user_id:
                rec.state = 'approve_hod'
    #            rec.hou_user_id = self.env.user.id
                rec.hou_approved_date_time = fields.Datetime.now()
            else:
                raise ValidationError("Please Select Your Coordinator")

    @api.multi
    def action_approve_offi(self):
        for rec in self:
            rec._check_reserved_vehicle()
            if rec.hou_user_id:
                rec.state = 'approve_offi'
#                rec.coordinator_user_id = self.env.user.id
                rec.coordinator_approved_date_time = fields.Datetime.now()
            else:
                raise ValidationError("Please Select Your Manager")

    @api.multi
    def action_reserve(self):
        for rec in self:
            rec._check_reserved_vehicle()
            rec.state = 'reserved'
#            rec.manager_user_id = self.env.user.id
            rec.manager_approved_date_time = fields.Datetime.now()
            if not self.reservation_schedule_ids:
                raise ValidationError("Please Choose Your Vehicle for ride")
            for schedule_id in self.reservation_schedule_ids:
                start_date = datetime.datetime.strptime(
                    schedule_id.start_date_time,
                    '%Y-%m-%d %H:%M:%S'
                )
                end_date = datetime.datetime.strptime(
                    schedule_id.end_date_time,
                    '%Y-%m-%d %H:%M:%S'
                )
                duration = (end_date - start_date).total_seconds()/3600

                vals = {'name': rec.reserving_employee_id.name +
                        " - " + rec.name,
                        'partner_ids': [(6, 0, rec.partner_id.ids)],
                        'start': schedule_id.start_date_time,
                        'stop': schedule_id.end_date_time,
                        'start_datetime': schedule_id.start_date_time,
                        'duration': duration,
                        'user_id': rec.env.uid,
                        'vehicle_id': schedule_id.vehicle_id.id,
                        'vehicle_reservation_id': rec.id,
                        'vehicle_type_id':
                        schedule_id.vehicle_type_id.id,
                        'vehicle_sub_type_id':
                        schedule_id.vehicle_sub_type_id.id,
                        'department_id': schedule_id.department_id.id,
                        'reservation_schedule_id': schedule_id.id,
                        'is_ride_share': rec.is_ride_share,
                        'rides_msg': rec.rides_msg,
                        'is_service_vehicle_reservation':
                        rec.is_service_vehicle_reservation,
                        'reservation_service_type_id':
                        rec.reservation_service_type_id.id,
                        'description': schedule_id.note,
#                        'deposit_charge_amount':
#                        schedule_id.deposit_charge_amount,
                        'is_reserve_for_other': rec.is_reserve_for_other,
                        'employee_present_status': rec.employee_present_status,
                        'person_phone': rec.person_phone,
                        'person_name': rec.person_name,
                        'vehicle_reserved_employee_id':
                        rec.reserving_employee_id.id,
                        'company_id':rec.company_id,
                        'rfid_key':rec.rfid_key,}
                event = rec.env['calendar.event'].create(vals)
                schedule_id.calendar_event_id = event.id
            if event:
                rec.calendar_event_ids += event

    @api.multi
    def action_cancle(self):
        for rec in self:
            rec.state = 'cancel'

    @api.multi
    def action_reject(self):
        for rec in self:
            rec.state = 'reject'

#    def daterange(start_date, end_date):
#        for n in range(int ((end_date - start_date).days)):
#            yield start_date + timedelta(n)

    def _pricelist_amount(self,pricelist_line,start_date,end_date,amount):
        if str(start_date) >= pricelist_line.start_date and str(start_date) <= pricelist_line.end_date:
            if str(end_date) >= pricelist_line.start_date and str(end_date) <= pricelist_line.end_date:
                if pricelist_line.pricelist_type == 'days':
                    if pricelist_line.day == start_date.strftime("%w"):
                        amount += (amount * pricelist_line.percentage) / 100
                        return amount
                elif pricelist_line.pricelist_type == 'hours':
                    start_hrs = float(start_date.hour) +\
                        (float(start_date.minute) / 60)
                    end_hrs = float(end_date.hour) +\
                        (float(end_date.minute) / 60)
                    if pricelist_line.start_time <= start_hrs and\
                        pricelist_line.end_time >= start_hrs:
                            if pricelist_line.start_time <= end_hrs and\
                            pricelist_line.end_time >= end_hrs:
                                amount += (
                                    amount * pricelist_line.percentage
                                ) / 100
                                return amount
                elif pricelist_line.pricelist_type == 'both':
                    if pricelist_line.day == start_date.strftime("%w"):
                        start_hrs = float(start_date.hour) +\
                        (float(start_date.minute) / 60)
                        end_hrs = float(end_date.hour) +\
                        (float(end_date.minute) / 60)
                        if pricelist_line.start_time <= start_hrs and pricelist_line.end_time >= start_hrs:
                            if pricelist_line.start_time <= end_hrs and pricelist_line.end_time >= end_hrs:
                                amount += (amount * pricelist_line.percentage) / 100
                                return amount
        return amount
#    def _create_invoice(self,
#                        rec,
#                        invoice_obj,
#                        invoice_line_obj,
#                        product_obj,
#                        flag,
#                        total_km,
#                        schedule):
#        flag = True
#        cost_ids = schedule.vehicle_id.vehicle_dest_cost_ids
#        amount = 0.0
#        for cost in cost_ids:
#            if total_km >= cost.from_dist and\
#                    total_km <= cost.to_dist:
#                    
##                amount = cost.price_km * total_km
#                amount = rec.company_id.currency_id.compute(cost.price_km, rec.currency_id) * total_km

#        if rec.pricelist_id:
#            start_date = datetime.datetime.strptime(
#                schedule.start_date_time,
#                '%Y-%m-%d %H:%M:%S'
#            )
#            end_date = datetime.datetime.strptime(
#                schedule.end_date_time,
#                '%Y-%m-%d %H:%M:%S'
#            )
#            for pricelist_line in\
#                rec.pricelist_id.vehicle_pricelist_line_ids.sorted(
#                    key=lambda r: r.id):
#                if pricelist_line.start_date and pricelist_line.end_date:
#                    amount=rec._pricelist_amount(pricelist_line,start_date,end_date,amount)
#                    break
#                else:
#                    if pricelist_line.pricelist_type == 'days':
#                        if pricelist_line.day == start_date.strftime("%w"):
#                            amount += (
#                                amount * pricelist_line.percentage) / 100
#                            break
#                    elif pricelist_line.pricelist_type == 'hours':
#                        start_hrs = float(start_date.hour) +\
#                            (float(start_date.minute) / 60)
#                        end_hrs = float(end_date.hour) +\
#                            (float(end_date.minute) / 60)
#                        if pricelist_line.start_time <= start_hrs and\
#                            pricelist_line.end_time >= start_hrs:
#                                if pricelist_line.start_time <= end_hrs and\
#                                pricelist_line.end_time >= end_hrs:
#                                    amount += (
#                                        amount * pricelist_line.percentage
#                                    ) / 100
#                                    break
#                    elif pricelist_line.pricelist_type == 'both':
#                        if pricelist_line.day == start_date.strftime("%w"):
#                            start_hrs = float(start_date.hour) +\
#                            (float(start_date.minute) / 60)
#                            end_hrs = float(end_date.hour) +\
#                            (float(end_date.minute) / 60)
#                            if pricelist_line.start_time <= start_hrs and pricelist_line.end_time >= start_hrs:
#                                if pricelist_line.start_time <= end_hrs and pricelist_line.end_time >= end_hrs:
#                                    amount += (amount * pricelist_line.percentage) / 100
#                                    break
##        product = product_obj.search(
##            [('is_vehicle', '=', True)],
##            limit=1
##        )
#        account_id = False
#        if schedule.vehicle_id.product_id:
#            account_id = schedule.vehicle_id.product_id.property_account_income_id or\
#                schedule.vehicle_id.product_id.categ_id.property_account_income_categ_id
#            line_vals = {
#                'product_id': schedule.vehicle_id.product_id.id,
#            }
#        else:
#            raise ValidationError("Please Select One product")

#        if not account_id:
#            raise ValidationError("No anyone account Found")

#        new_line = invoice_line_obj.new({'product_id': schedule.vehicle_id.product_id.id})
#        new_line._onchange_product_id()
#        
#        taxes_id = schedule.vehicle_id.product_id.taxes_id
#        fpos = schedule.partner_id.property_account_position_id
#        if fpos:
#            taxes_id = fpos.map_tax(schedule.vehicle_id.product_id.taxes_id, schedule.vehicle_id.product_id, schedule.partner_id)

#        line_vals.update({
#            'name': rec.name + " - " + schedule.vehicle_id.name +
#            " is reserved from " + schedule.start_date_time +
#            " to " + schedule.start_date_time,
#            'quantity': 1,
#            'invoice_line_tax_ids':[(6, 0, taxes_id.ids)],
#            'price_unit': amount,
#            'account_id': account_id.id,
#            'vehicle_id': schedule.vehicle_id.id,
#            'reservation_schedule_id': schedule.id,
#        })
#        line_ids = invoice_line_obj.create(line_vals)

#        default_fields = [
#            'user_id',
#            'journal_id',
#            'company_id',
#        ]
#        invoice_vals = invoice_obj.default_get(default_fields)
#        invoice_vals.update({
#            'partner_id': rec.partner_id.id,
#            'currency_id':rec.currency_id.id,
#            'date_invoice': fields.Datetime.now(),
#            'invoice_line_ids': [(6, 0, line_ids.ids)],
#            'reservation_employee_id': rec.reserving_employee_id.id,
#            'department_id': rec.department_id.id,
#            'vehicle_reservation_id': rec.id,
#            'is_reservation_invoice': True,
#        })
#        invoice = invoice_obj.new(invoice_vals)
#        invoice._onchange_partner_id()
#        invoice_vals.update({'account_id': invoice.account_id.id,
#                             'comment': schedule.note})
#        invoice = invoice_obj.create(invoice_vals)

#        schedule.invoice_id = invoice
#        rec.acount_invoice_ids += invoice
#        return flag

#    @api.multi
#    def action_create_invoice(self):
#        invoice_obj = self.env['account.invoice']
#        invoice_line_obj = self.env['account.invoice.line']
#        product_obj = self.env['product.product']
#        for rec in self:
#            if rec.is_service_vehicle_reservation:
#                raise ValidationError("This Reservation is for \
#                the vehicle service you can't generate invoice")

#            if rec.reserving_employee_id.open_invoice_due_date:
#                due_date = datetime.datetime.strptime(
#                    rec.reserving_employee_id.open_invoice_due_date,"%Y-%m-%d %H:%M:%S"
#                )
#                block_date = due_date +\
#                    timedelta(days=rec.company_id.reserve_block_days)
#                if str(block_date) <= fields.Datetime.now():
#                    raise ValidationError(_("You were block please pay last\
#                        invoice")
#                    )

#            flag = False
#            #Count  Invoice Total Amount
#            inv_amount = sum(rec.reservation_schedule_ids.filtered(
#                lambda i: i.invoice_id.state == 'cancel' or not
#                i.invoice_id).mapped('invoice_amount_to_pay'))

#            for schedule in rec.reservation_schedule_ids:
#                total_km = schedule.total_km
#                if schedule.is_return and not schedule.invoice_id:
#                    flag = rec._create_invoice(
#                        rec,
#                        invoice_obj,
#                        invoice_line_obj,
#                        product_obj,
#                        flag,
#                        total_km,
#                        schedule)

#                if schedule.is_return and schedule.invoice_id:
#                    if schedule.invoice_id.state == 'cancel':
#                        flag = rec._create_invoice(
#                            rec,
#                            invoice_obj,
#                            invoice_line_obj,
#                            product_obj,
#                            flag,
#                            total_km,
#                            schedule)

#            if not flag:
#                raise ValidationError("No any Reservation for invoice")

#            if all([x.invoice_id for x in rec.reservation_schedule_ids]):
#                rec.state = "invoice"

    @api.multi
    def action_calendar_event(self):
        for rec in self:
            events = rec.mapped('calendar_event_ids')
            action = rec.env.ref('calendar.action_calendar_event').read()[0]
            action['domain'] = [('id', 'in', events.ids)]
            return action

    @api.multi
    def action_invoice(self):
        invoice = self.mapped('acount_invoice_ids')
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['domain'] = [('id', 'in', invoice.ids)]
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
