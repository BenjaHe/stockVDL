# -*- coding: utf-8 -*-

from openerp import api, fields, models

class SaleOrder(models.Model):
    _inherit = ['sale.order']

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('validation_1', 'Validation premier niveau'),
        ('validation_2', 'Validation deuxième niveau'),
        ('sale', 'Sale Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], help='Etat de la demande d achat. L état en bleu est l etat actuel de la validation.')

    customer_comment_num_engagement = fields.Char(string="Numéro d'engagement renseigné par le client du webshop", required= False)