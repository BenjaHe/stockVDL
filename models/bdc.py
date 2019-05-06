# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning


class ResPartner(models.Model):
    _inherit = ['res.partner']

    comptable = fields.Many2one('res.users', string='Comptable attitré', required=False, track_visibility='onchange')
    directeur = fields.Many2one('res.users', string='Directeur validateur', required=False, track_visibility='onchange')
    num_comptable = fields.Char(string='Numéro du comptable', required=False, track_visibility='onchange', help='A renseigner uniquement pour les comptables.')
    num_mon_comptable = fields.Char(string='Numéro de mon comptable', required=False, related='comptable.num_comptable', help='Le numéro du comptable qui m est renseigné.')

class Sale(models.Model):
    _inherit = ['sale.order']

    comptable_id = fields.Many2one("res.users", related='partner_id.comptable', string="Comptable", readonly=True,
                                   required=False)
    directeur_id = fields.Many2one("res.users", related='partner_id.directeur', string="Directeur", readonly=True,
                                   required=False)


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    directeur_id = fields.Many2one("res.users", related='dest_address_id.directeur', string="Directeur",
                                   readonly=True,
                                   required=False)
    comptable_id = fields.Many2one("res.users", related='dest_address_id.comptable', string="Directeur",
                                   readonly=True,
                                   required=False)
    tel_comptable_id = fields.Char("res.users", related='dest_address_id.comptable.mobile',
                                   readonly=True,
                                   required=False)
    num_comptable_id = fields.Char("res.users", related='dest_address_id.comptable.num_comptable',
                                   readonly=True,
                                  required=False)

class Product(models.Model):
    _inherit = ['product.template']

    # Ajout d'un prix TVAC (21 %) --> car les prix sont tous HTVA en ce compris sur le site web

    prix_tvac = fields.Monetary(compute='_prix_tvac', string ='Prix TVAC (21 %)')

    @api.depends('list_price')
    def _prix_tvac(self):
        for product in self:
            product.prix_tvac = product.list_price * 1.21

class invoice(models.Model):
    _inherit = ['account.invoice']

    @api.one
    def bouton_draft(self):
        self.write({
            'state': 'draft'
        })
