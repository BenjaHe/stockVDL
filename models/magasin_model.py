# -*- coding: utf-8 -*-

from openerp import models, fields

class CommentaireMagasinier (models.Model):
    _inherit = 'stock.picking'
    commentaire = fields.Char('Commentaire pour la livraison', required=False)
