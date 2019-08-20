# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions


class ProcurementOrder(models.Model):
    _inherit='procurement.order'

    @api.multi
    def make_po(self):
        res = super(ProcurementOrder, self).make_po()
        procurements=self.browse(res)                  # on récupère la liste des procurements traité par make_po
        procurements.propagate_so_info()               # on lui rajoute notre méthode

        return res

    @api.multi
    def propagate_so_info(self):   # le self est ici notre liste de procurements donc on va faire une boucle
        for proc in self:
            if proc.sale_line_id and proc.purchase_id:
                vals={'article_budgetaire':proc.sale_line_id.order_id.customer_comment_num_article,
                      'num_engagement':proc.sale_line_id.order_id.customer_comment_num_engagement,
                      'date_livraison_souhaite':proc.sale_line_id.order_id.date_livraison_souhaite}
                proc.purchase_id.write(vals)
        return



