# -*- coding: utf-8 -*-

from operator import itemgetter
from datetime import datetime

from openerp import api, fields, models, _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    _description = 'Budget_Type'

    payment_acquirer_id_budget = fields.Many2one(comodel_name='payment.acquirer',
                                                 string='Payment acquirer',
                                                # related='payment_acquirer_id.payment_acquirer_id_budget',
                                                 required=False)