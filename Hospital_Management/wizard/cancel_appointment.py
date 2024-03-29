import datetime
from datetime import date
from dateutil import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment",
                                     domain=['|', ('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('Hospital_Management.cancel_day')
        print("cancel_day", cancel_day)
        allow_today = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if cancel_day != 0 and allow_today < date.today():
            raise ValidationError(_("Sorry, this cancellation is not allowed for this booking"))
        self.appointment_id.state = 'cancel'
        return {'type': 'ir.actions.client', 'tag': 'reload'}
        # if self.appointment_id.booking_date == fields.Date.today():
        #     raise ValidationError(_("Sorry, cancellation is not allowed on the same"))
        # self.appointment_id.state = 'cancel'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res
