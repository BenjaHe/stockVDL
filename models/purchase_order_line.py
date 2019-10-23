# -*- coding: utf-8 -*-

from openerp import api, fields, models

class PurchaseOrderline(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _description = "Purchase Line Custom for Microsoft Dynamics"

    dyn_orderaccount = fields.Integer(string="Id Dyn du fournisseur",
                                      required=False)
    dyn_buyergroupid = fields.Integer(related='order_id.directeur',
                                      string="Num Dyn du CP",
                                      required=False)
    dyn_taxCode = fields.Char(related='product_id.dyn_taxe',
                              string="Id Dyn de la taxe",
                              required=False)

