# -*- coding: utf-8 -*-

from operator import itemgetter
from datetime import datetime

from openerp import api, fields, models, _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Partner'

    # Le champs "budget_test" aurait dû s'appler "budget" mais ayant eu des déboires pour le créer,
    # quand j'ai réussi à créer "budget_test", j'ai gardé celui-ci
    # Le champs total_invoiced est la reprise du calcul fait plus bas de la sommes des factures TVAC de l'année en cours
    budget_test = fields.Monetary('Budget en cours', required=False)
    total_invoiced_tvac = fields.Monetary(compute='_invoice_total_tvac', string="Total Invoiced",
                                          groups='account.group_account_invoice')

    @api.multi
    def _invoice_total_tvac(self):
        account_invoice = self.env['account.invoice']
        if not self.ids:
            self.total_invoiced_TVAC = 0.0
            return True

        today = '%d0101' % datetime.today().year

        user_currency_id = self.env.user.company_id.currency_id.id
        all_partners_and_children = {}
        all_partner_ids = []
        for partner in self:
            # price_total is in the company currency
            all_partners_and_children[partner] = self.with_context(active_test=False).search(
                [('id', 'child_of', partner.id)]).ids
            all_partner_ids += all_partners_and_children[partner]

        # searching account.invoice.report via the orm is comparatively expensive
        # (generates queries "id in []" forcing to build the full table).
        # In simple cases where all invoices are in the same currency than the user's company
        # access directly these elements

        # generate where clause to include multicompany rules
        # PROBLEME DE FILTRE SUR ANNEE EN COURS :
        where_query = account_invoice._where_calc([
            ('partner_id', 'in', all_partner_ids), ('state', 'not in', ['draft', 'cancel']),
            ('type', 'in', ('out_invoice', 'out_refund')), ('date', '>=', today)
        ])
        account_invoice._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        # price_total is in the company currency
        query = """
              SELECT SUM(amount_total_signed) as total, partner_id
                FROM account_invoice account_invoice
               WHERE %s
               GROUP BY partner_id
            """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            partner.total_invoiced_tvac = sum(price['total']
                                              for price in price_totals if price['partner_id'] in child_ids)

    # Calcul du budget restant qui est la différence entre le budget donné et la somme des factures de l'année en
    # cours TVAC

    budget_restant = fields.Monetary(compute='_compute_budget_restant', string="Budget restant")

    @api.depends('total_invoiced_tvac', 'budget_test')
    def _compute_budget_restant(self):
        for partner in self:
            partner.budget_restant = partner.budget_test - partner.total_invoiced_tvac
