# -*- coding: utf-8 -*-

from openerp import api, fields, models

class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _description = "Purchase Order Custom Workflow"

    VALUES = [('validation_1', 'Validation premier niveau'),
              ('validation_2', 'Validation deuxième niveau')]

    state = fields.Selection(selection_add=VALUES)

