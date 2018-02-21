# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

import datetime
import pytz
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ReservationScheduleInvoiceWiz(models.TransientModel):
    _name = "reservation.schedule.invoice.wiz"


    def _create_invoice(self,
                        rec,
                        invoice_obj,
                        invoice_line_obj,
                        product_obj,
                        flag,
                        total_km,
                        total_hr,
                        schedule,
                        line_ids,
                        prolog=False):
        flag = True
        cost_ids = schedule.vehicle_id.vehicle_dest_cost_ids
        time_cost_ids = schedule.vehicle_id.vehicle_time_cost_ids
        amount = 0.0
        line_description = " "
        line_vals = {}
        start_date = datetime.datetime.strptime(
            schedule.start_date_time,
            '%Y-%m-%d %H:%M:%S'
        )
        end_date = datetime.datetime.strptime(
            schedule.end_date_time,
            '%Y-%m-%d %H:%M:%S'
        )
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        sch_tzone_start_date = pytz.UTC.localize(start_date)
        sch_start_date_tz = sch_tzone_start_date.astimezone(timezone)
        
        sch_tzone_end_date = pytz.UTC.localize(end_date)
        sch_end_date_tz = sch_tzone_end_date.astimezone(timezone)
        if not prolog:
            line_description = rec.name + " - " + schedule.vehicle_id.name +\
            " is reserved from " + str(sch_start_date_tz).split('+')[0] +\
            " to " + str(sch_end_date_tz).split('+')[0]
            if schedule.billing_type == 'per_km':
                for cost in cost_ids:
                    if total_km >= cost.from_dist and\
                            total_km <= cost.to_dist:
#                        amount = rec.company_id.currency_id.compute(cost.price_km, rec.currency_id) * total_km
                        amount = rec.company_id.currency_id.compute(cost.price_km, rec.currency_id)
                    else:
                        max_dist =  max([cost.to_dist for cost in cost_ids])
                        cost_id = cost_ids.search([('to_dist','=',max_dist)])
                        amount = rec.company_id.currency_id.compute(cost_id.price_km, rec.currency_id)
                line_vals.update({'quantity': total_km,})
            elif schedule.billing_type == 'per_hr':
                for cost in time_cost_ids:
                    if total_hr >= cost.from_hour and\
                            total_hr <= cost.to_hour:
#                        amount = rec.company_id.currency_id.compute(cost.price_hour, rec.currency_id) * total_hr
                        amount = rec.company_id.currency_id.compute(cost.price_hour, rec.currency_id)
                    else:
                        max_hr =  max([cost.to_hour for cost in time_cost_ids])
                        cost_id = time_cost_ids.search([('to_hour','=',max_hr)])
                        amount = rec.company_id.currency_id.compute(cost_id.price_hour, rec.currency_id)
                line_vals.update({'quantity': total_hr,})
        else:
            amount = rec.company_id.currency_id.compute(total_km, rec.currency_id)
            line_vals.update({'quantity': schedule.prolog_hours,})
            line_description = "Prolog Penalty due to delayed"

#                amount = cost.price_km * total_km
        if rec.pricelist_id:
            for pricelist_line in\
                rec.pricelist_id.vehicle_pricelist_line_ids.sorted(
                    key=lambda r: r.id):
                if pricelist_line.start_date and pricelist_line.end_date:
                    amount=rec._pricelist_amount(pricelist_line,start_date,end_date,amount)
                    break
                else:
                    if pricelist_line.pricelist_type == 'days':
                        if pricelist_line.day == start_date.strftime("%w"):
                            amount += (
                                amount * pricelist_line.percentage) / 100
                            break
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
                                    break
                    elif pricelist_line.pricelist_type == 'both':
                        if pricelist_line.day == start_date.strftime("%w"):
                            start_hrs = float(start_date.hour) +\
                            (float(start_date.minute) / 60)
                            end_hrs = float(end_date.hour) +\
                            (float(end_date.minute) / 60)
                            if pricelist_line.start_time <= start_hrs and pricelist_line.end_time >= start_hrs:
                                if pricelist_line.start_time <= end_hrs and pricelist_line.end_time >= end_hrs:
                                    amount += (amount * pricelist_line.percentage) / 100
                                    break
        account_id = False
        if schedule.vehicle_id.product_id:
            account_id = schedule.vehicle_id.product_id.property_account_income_id or\
                schedule.vehicle_id.product_id.categ_id.property_account_income_categ_id
            if schedule.billing_type == 'per_km':
                line_vals.update({
                    'product_id': schedule.vehicle_id.product_id.id,
                    'uom_id':schedule.vehicle_id.product_id.uom_id.id
                })
            elif schedule.billing_type == 'per_hr':
                line_vals.update({
                    'product_id': schedule.vehicle_id.product_hour_id.id,
                    'uom_id':schedule.vehicle_id.product_hour_id.uom_id.id
                })
            if prolog:
                line_vals.update({
                    'uom_id':schedule.vehicle_id.product_hour_id.uom_id.id
                })
        else:
            raise ValidationError("Please Set One Account")
        if not account_id:
            raise ValidationError("Please Set One Account")

        new_line = invoice_line_obj.new({'product_id': schedule.vehicle_id.product_id.id})
        new_line._onchange_product_id()

        taxes_id = schedule.vehicle_id.product_id.taxes_id
        fpos = schedule.invoice_partner_id.property_account_position_id
        if fpos:
            taxes_id = fpos.map_tax(schedule.vehicle_id.product_id.taxes_id, schedule.vehicle_id.product_id, schedule.invoice_partner_id)

        line_vals.update({
            'name': line_description,
#            'quantity': 1,
            'invoice_line_tax_ids':[(6, 0, schedule.vehicle_id.product_id.taxes_id.ids)],
            'price_unit': amount,
            'account_id': account_id.id,
            'vehicle_id': schedule.vehicle_id.id,
            'reservation_schedule_id': schedule.id,
        })
        line_ids += invoice_line_obj.create(line_vals)

        return flag, line_ids


    @api.multi
    def action_create_invoice(self):
        for rec in self:
            active_ids = rec._context.get("active_ids")
            if len(active_ids) == 1:
                active_ids.append(0)
            invoice_obj = self.env['account.invoice']
            invoice_line_obj = self.env['account.invoice.line']
            product_obj = self.env['product.product']
            invoice_ids = invoice_obj
            res_schedule = rec.env['vehicle.reservation.schedule'].search([('id', 'in', active_ids),('is_return','=',True)])
            old_mnth = []
            invoice_amount = 0.0
            create_invoice = False
            
            date_query = ("""
                    SELECT
                        line.reservation_date as date,
                        line.invoice_partner_id
                    FROM
                        vehicle_reservation_schedule as line
                    WHERE
                        line.id IN %s
                    GROUP BY
                        date,
                        line.invoice_partner_id
            """)
            self.env.cr.execute(date_query  %(tuple(active_ids),))
            date_query_results = self.env.cr.dictfetchall()
            reserv_month_dict = {}
            for date_partner_dict in date_query_results:
                date_partner = date_partner_dict.get('invoice_partner_id')
                date = date_partner_dict.get('date')
                reservation_date = datetime.datetime.strptime(
                    date,
                    '%Y-%m-%d'
                )
                if not date_partner in reserv_month_dict:
                    old_mnth.append(reservation_date)
                    reserv_month_dict.update({date_partner:len(old_mnth)})
                else:
                    if reserv_month_dict.get(date_partner) == reservation_date.month:
                        reserv_month_dict[date_partner] = len(old_mnth)
                    else:
                        old_mnth.append(reservation_date)
                        reserv_month_dict[date_partner] = len(old_mnth)
            query = ("""
                    SELECT
                        sum(line.invoice_amount_to_pay),
                        line.invoice_partner_id
                    FROM
                        vehicle_reservation_schedule as line
                    WHERE
                        line.id IN %s
                    GROUP BY
                        line.invoice_partner_id
            """)
            self.env.cr.execute(query  %(tuple(active_ids),))
            query_results = self.env.cr.dictfetchall()
            invoice_partner_dict = {}
            for partner in query_results:
                partner_id = partner.get('invoice_partner_id')
                invoice_sum = partner.get('sum')
                if not invoice_sum == None:
                    invoice_partner_dict.update({partner_id:float(invoice_sum)})

            month_cnt = len(old_mnth)

            partner_id = rec.env['res.partner']
            cont_invoice = invoice_obj
            partner_lst = []
            for schedule_id in active_ids:
                schedule = rec.env['vehicle.reservation.schedule'].browse(int(schedule_id))
                total_km = schedule.total_km
                total_hr = schedule.total_hour
                flag = False
                line_ids = invoice_line_obj
                if schedule.fleet_vehicle_reservation_id.is_service_vehicle_reservation:
                    continue

                if schedule.is_return and not schedule.invoice_id:
                    if (schedule.invoice_partner_id.id in reserv_month_dict and reserv_month_dict.get(schedule.invoice_partner_id.id) >= schedule.company_id.allow_minimum_month_invoice) or (invoice_partner_dict.get(schedule.invoice_partner_id.id) and invoice_partner_dict.get(schedule.invoice_partner_id.id) >= schedule.company_id.invoice_amount):
                        if not schedule.invoice_partner_id in partner_lst:
                            partner_lst.append(schedule.invoice_partner_id)
                            flag, line_ids = rec._create_invoice(
                                schedule.fleet_vehicle_reservation_id,
                                invoice_obj,
                                invoice_line_obj,
                                product_obj,
                                flag,
                                total_km,
                                total_hr,
                                schedule,
                                line_ids)
                                
                            if not schedule.extra_time_no_reservation:
                                prolog_amount = schedule.vehicle_id.billing_multiplier
                                prolog = True
                                flag, line_ids = rec._create_invoice(
                                    schedule.fleet_vehicle_reservation_id,
                                    invoice_obj,
                                    invoice_line_obj,
                                    product_obj,
                                    flag,
                                    prolog_amount,
                                    total_hr,
                                    schedule,
                                    line_ids,
                                    prolog)
                            partner_id = schedule.invoice_partner_id
                            default_fields = [
                                'user_id',
                                'journal_id',
                                'company_id',
                            ]
                            invoice_vals = invoice_obj.default_get(default_fields)
                            invoice_vals.update({
                                'partner_id': schedule.invoice_partner_id.id,
                                'reservation_employee_id': schedule.employee_id.id,
                                'department_id': schedule.department_id.id,
                                'currency_id': schedule.fleet_vehicle_reservation_id.currency_id.id,
                                'date_invoice': fields.Datetime.now(),
                                'invoice_line_ids': [(6, 0, line_ids.ids)],
                                'is_reservation_invoice': True,
                            })
                            invoice = invoice_obj.new(invoice_vals)
                            invoice._onchange_partner_id()
                            invoice_vals.update({'account_id': invoice.account_id.id,
                                                 'comment': schedule.note})
                            cont_invoice = invoice_obj.create(invoice_vals)
                            schedule.invoice_id = cont_invoice.id
                            schedule.fleet_vehicle_reservation_id.acount_invoice_ids += cont_invoice
                            invoice_ids += cont_invoice
                        else:
                            if not cont_invoice.currency_id == schedule.fleet_vehicle_reservation_id.currency_id:
                                raise ValidationError("Some Reservation in Different Currency")
                            else:
                                flag, line_ids = rec._create_invoice(
                                    schedule.fleet_vehicle_reservation_id,
                                    invoice_obj,
                                    invoice_line_obj,
                                    product_obj,
                                    flag,
                                    total_km,
                                    total_hr,
                                    schedule,
                                    line_ids)
                                if not schedule.extra_time_no_reservation:
                                    prolog_amount = schedule.vehicle_id.billing_multiplier
                                    prolog = True
                                    flag, line_ids = rec._create_invoice(
                                        schedule.fleet_vehicle_reservation_id,
                                        invoice_obj,
                                        invoice_line_obj,
                                        product_obj,
                                        flag,
                                        prolog_amount,
                                        total_hr,
                                        schedule,
                                        line_ids,
                                        prolog)
                                invoice = invoice_ids.filtered(lambda x:x.partner_id == schedule.invoice_partner_id)
                                invoice.invoice_line_ids += line_ids
                                schedule.invoice_id = invoice.id
                    else:
                        continue
                if schedule.is_return and schedule.invoice_id:
                    reserv_month_dict
                    if schedule.invoice_id.state == 'cancel':
                        if (schedule.invoice_partner_id.id in reserv_month_dict and reserv_month_dict.get(schedule.invoice_partner_id.id) >= schedule.company_id.allow_minimum_month_invoice) or (invoice_partner_dict.get(schedule.invoice_partner_id.id) and invoice_partner_dict.get(schedule.invoice_partner_id.id) >= schedule.company_id.invoice_amount):
                            if not schedule.invoice_partner_id in partner_lst:
                                partner_lst.append(schedule.invoice_partner_id)
                                flag, line_ids = rec._create_invoice(
                                    schedule.fleet_vehicle_reservation_id,
                                    invoice_obj,
                                    invoice_line_obj,
                                    product_obj,
                                    flag,
                                    total_km,
                                    total_hr,
                                    schedule,
                                    line_ids)
                                if not schedule.extra_time_no_reservation:
                                    prolog_amount = schedule.vehicle_id.billing_multiplier
                                    prolog = True
                                    flag, line_ids = rec._create_invoice(
                                        schedule.fleet_vehicle_reservation_id,
                                        invoice_obj,
                                        invoice_line_obj,
                                        product_obj,
                                        flag,
                                        prolog_amount,
                                        total_hr,
                                        schedule,
                                        line_ids,
                                        prolog)
                                default_fields = [
                                    'user_id',
                                    'journal_id',
                                    'company_id',
                                ]
                                invoice_vals = invoice_obj.default_get(default_fields)
                                invoice_vals.update({
                                    'partner_id': schedule.invoice_partner_id.id,
                                    'reservation_employee_id': schedule.employee_id.id,
                                    'department_id': schedule.department_id.id,
                                    'currency_id':schedule.fleet_vehicle_reservation_id.currency_id.id,
                                    'date_invoice': fields.Datetime.now(),
                                    'invoice_line_ids': [(6, 0, line_ids.ids)],
                                    'is_reservation_invoice': True,
                                })
                                invoice = invoice_obj.new(invoice_vals)
                                invoice._onchange_partner_id()
                                invoice_vals.update({'account_id': invoice.account_id.id,
                                                     'comment': schedule.note})
                                cont_invoice = invoice_obj.create(invoice_vals)
                                schedule.invoice_id = cont_invoice.id
                                schedule.fleet_vehicle_reservation_id.acount_invoice_ids += cont_invoice
                                invoice_ids += cont_invoice
                            else:
                                if not cont_invoice.currency_id == schedule.fleet_vehicle_reservation_id.currency_id:
                                    raise ValidationError("Some Reservation in Different Currency")
                                else:
                                    flag, line_ids = rec._create_invoice(
                                        schedule.fleet_vehicle_reservation_id,
                                        invoice_obj,
                                        invoice_line_obj,
                                        product_obj,
                                        flag,
                                        total_km,
                                        total_hr,
                                        schedule,
                                        line_ids)
                                    if not schedule.extra_time_no_reservation:
                                        prolog_amount = schedule.vehicle_id.billing_multiplier
                                        prolog = True
                                        flag, line_ids = rec._create_invoice(
                                            schedule.fleet_vehicle_reservation_id,
                                            invoice_obj,
                                            invoice_line_obj,
                                            product_obj,
                                            flag,
                                            prolog_amount,
                                            total_hr,
                                            schedule,
                                            line_ids,
                                            prolog)
                                    invoice = invoice_ids.filtered(lambda x:x.partner_id == schedule.invoice_partner_id)
                                    invoice.invoice_line_ids += line_ids
                                    schedule.invoice_id = invoice.id
                        else:
                            continue
                if all([x.invoice_id for x in schedule.fleet_vehicle_reservation_id.reservation_schedule_ids]):
                    if schedule:
                        schedule.fleet_vehicle_reservation_id.state = "invoice"

            if invoice_ids:
                action = self.env.ref('account.action_invoice_tree1').read()[0]
                action['domain'] = [('id', 'in', invoice_ids.ids)]
                return action

            if not flag:
                raise ValidationError("Invoice Allready Created or It's not return or It was service reservation")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
