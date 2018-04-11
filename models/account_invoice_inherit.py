# -*- coding: utf-8 -*-

from operator import itemgetter
from datetime import datetime

from openerp import api, fields, models, _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    _description = 'Invoice'

    payment_acquired_id_budget = fields.Many2one('payment.acquirer', 'budget_type', required=False)