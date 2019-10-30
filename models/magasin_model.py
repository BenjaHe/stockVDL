# -*- coding: utf-8 -*-


from openerp import models, fields

class CommentaireMagasinier (models.Model):
    _inherit = 'stock.picking'
    commentaire = fields.Char('Commentaire pour la livraison', required=False)

    # Champs boolean pour indiquer aux magasiners si le staff administratif a vérifié que le client a encore du budget

    ok_livraison = fields.Boolean(string='La commande peut être préparée', default=False, track_visibility='onchange')


