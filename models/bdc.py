# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
from openerp import models, fields, api, exceptions
from openerp.addons.website_sale.models.product import product_public_category
from openerp.exceptions import Warning


class ResPartner(models.Model):
    _inherit = ['res.partner']

    comptable = fields.Many2one('res.users', string='Comptable principal', required=False, track_visibility='onchange')
    comptables = fields.Many2many('res.users', string='Comptables autorisés', required=False, track_visibility='onchange')

    directeur = fields.Many2one('res.users', string='Directeur validateur', required=False, track_visibility='onchange')
    num_comptable = fields.Char(string='Numéro du comptable', required=False, track_visibility='onchange', help='A renseigner uniquement pour les comptables.')
    num_mon_comptable = fields.Char(string='Numéro de mon comptable', required=False, related='comptable.num_comptable', help='Le numéro du comptable qui m est renseigné.')
    fournisseur_economat = fields.Boolean(string='Est un fournisseur de l économat', store=True, required=False, track_visibility='onchange')

    # Champs Dynamics qui donne les références Dyn du fournisseur
    dyn_buyergroupid = fields.Char(string="Comptable dans Dynamics", required=False, track_visibility='onchange')


class Sale(models.Model):
    _inherit = ['sale.order']

    comptable_id = fields.Many2one("res.users", related='partner_id.comptable', string="Comptable principal", readonly=True,
                                   required=False)
    comptable_ids = fields.Many2many("res.users", related='partner_id.comptables', string="Comptables autorisés", readonly=True,
                                     required=False)
    directeur_id = fields.Many2one("res.users", related='partner_id.directeur', string="Directeur", readonly=True,
                                   required=False)


class SaleOrder(models.Model):
    _inherit = ['sale.order.line']


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    directeur_id = fields.Many2one("res.users", related='dest_address_id.directeur',
                                   string="Directeur",
                                   readonly=True,
                                   required=False)
    comptable_id = fields.Many2one("res.users", related='dest_address_id.comptable',
                                   string="Comptable principal",
                                   readonly=True,
                                   required=False)
    comptable_ids = fields.Many2many("res.users",
                                     related='dest_address_id.comptables',
                                     string="Comptables autorisés", readonly=True,
                                     required=False)
    tel_comptable_id = fields.Char("res.users",
                                   related='dest_address_id.comptable.mobile',
                                   readonly=True,
                                   required=False)
    num_comptable_id = fields.Char("res.users",
                                   related='dest_address_id.comptable.num_comptable',
                                   readonly=True,
                                   required=False)

    fournisseur_economat = fields.Boolean(related='partner_id.fournisseur_economat',
                                          string='Est un fournisseur de l économat',
                                          readonly=True,
                                          required=False)

    dyn_buyergroupid = fields.Char(string="Comptable dans Dynamics",
                                     readonly=True,
                                     required=False)

class Product(models.Model):
    _inherit = ['product.template']

    # Id de la taxe - taxgroup - de l'article dans Microsoft Dyn (utilisé pour pousser les commandes dans Dyn)
    dyn_taxgroup = fields.Char(string="Champs TaxGroup issu de Dynamics",
                               required=False)

    # Id de la taxe - taxitemgroup - de l'article dans Microsoft Dyn (utilisé pour pousser les commandes dans Dyn)
    dyn_taxitemgroup = fields.Char(string="Champs TaxGroup issu de Dynamics",
                                   required=False)

    # Ajout d'un prix TVAC (21 %) --> car les prix sont tous HTVA en ce compris sur le site web
    prix_tvac = fields.Monetary(compute='_prix_tvac',
                                string ='Prix TVAC (21 % - pour info)',
                                help="A titre informatif car le calcul "
                                     "des commandes se fait sur base du prix HTVA.")

    # Affichage du prix public TVAC
    prix_public_tvac = fields.Monetary(string="Prix public TVAC")

    # Affichage du prix réduit TVAC
    prix_reduc_tvac = fields.Monetary(string="Prix réduit TVAC")

    # Affichage du prix public TVAC
    prix_public_tvac = fields.Monetary(string="Prix public TVAC",
                                       help="Prix public TVAC du produit tel "
                                            "qu'exposer à un acheteur hors marché VDL.")

    # Affichage du prix réduit TVAC
    prix_reduc_tvac = fields.Monetary(string="Prix réduit TVAC",
                                      help="Prix VDL suite au marché "
                                           "(réduction appliquée) avec l'application de la TVA.")

    @api.depends('list_price')
    def _prix_tvac(self):
        for product in self:
            product.prix_tvac = product.list_price * 1.21

    # Retrait des 7% de remise IDEMA et ajout 21% TVA
    # def _prix_public_idema(self):
    #     if self.seller_ids.name == 'IDEMA-SPORT':
    #         for product in self:
    #             product.prix_public = (product.list_price / 93) * 121


class invoice(models.Model):
    _inherit = ['account.invoice']

    @api.one
    def bouton_draft(self):
        self.write({
            'state': 'draft'
        })
