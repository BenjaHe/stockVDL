# -*- coding: utf-8 -*-

from openerp import api, fields, models

class PurchaseOrderline(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _description = "Purchase Line Custom for Microsoft Dynamics"

    dyn_orderaccount_id = fields.Char(related='order_id.dyn_orderaccount',
                                      string="Id Dyn du fournisseur",
                                      required=False)
    dyn_buyergroupid_id = fields.Char(related='order_id.dyn_buyergroupid_id',
                                       string="Comptable dans Dynamics",
                                       required=False)
    dyn_taxgroup_id = fields.Char(related='product_id.dyn_taxgroup',
                              string="Champs TaxGroup issu de Dynamics",
                              required=False)

    dyn_taxitemgroup_id = fields.Char(related='product_id.dyn_taxitemgroup',
                               string="Champs TaxGroup issu de Dynamics",
                               required=False)

    dyn_state = fields.Selection([('None', 'Brouillon'),
                                  ('Backorder', 'Bon de commande créé'),
                                  ('Received', 'Commande reçue par le fournisseur'),
                                  ('Invoiced', 'En cours de livraison'),
                                  ('Canceled','Annulé')],
                                  string='Statut Dynamics de la ligne',
                                  default='None',
                                  store=True,
                                  track_visibility='onchange')

    dyn_purchid = fields.Integer(string="Champs PurchID dans Dynamics",
                                 required=False)

# class AccountTax(models.Model):
#     _name = "account.tax"
#     _inherit = "account.tax"
#     _description = "Tax custom attribute from Dynamics"
#
#     taxgroup = fields.Char(string="Champs TaxGroup issu de Dynamics", required=False)
#     taxitemgroup = fields.Char(string="Champs taxItemGroup issu de Dynamics", required=False)