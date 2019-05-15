# -*- coding: utf-8 -*-

from openerp import models, fields

class CommentaireMagasinier (models.Model):
    _inherit = 'stock.picking'
    commentaire = fields.Char('Commentaire pour la livraison', required=False)

    # Champs boolean pour indiquer aux magasiners si le staff administratif a vérifié que le client a encore du budget

    ok_livraison = fields.Boolean('Le client peut être livré', default=False, track_visibility='onchange')

    budget_restant = fields.Monetary(related='partner_id.parent_id.parent_id.budget_restant_CE', string='Budget restant (économat)')

