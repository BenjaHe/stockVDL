# -*- coding: utf-8 -*-

from operator import itemgetter
from datetime import datetime

from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Partner'

    # Le champs "budget_test" aurait dû s'appler "budget" mais ayant eu des déboires pour le créer,
    # quand j'ai réussi à créer "budget_test", j'ai gardé celui-ci
    # Le champs total_invoiced est la reprise du calcul fait plus bas de la sommes des factures TVAC de l'année en cours

    # budget_test : budget CP+CE et u total de toutes les factures TVAC de l'année en cours
    # budget - total CP : calcul sur le budget "Crédit Propre" : CP
    # budget - total CE : calcul sur le budget "Crédit Economat" : CE


    budget_test = fields.Monetary('Budget en cours', required=False)

    total_invoiced_tvac = fields.Monetary(compute='_invoice_total_tvac', string="Total Invoiced",
                                          groups='account.group_account_invoice')



    # CPapier   ########################################################################################################

    budget_CP = fields.Monetary(string='Budget Papier', required=False)
    total_invoiced_tvac_CP = fields.Monetary(compute='_invoice_total_tvac_CP', string="Total Invoiced CP")
    budget_restant_CP = fields.Monetary(compute='_compute_budget_restant_CP', string="Budget restant pour le Papier")

        # Champs pour l'exposition sur le site Web -------------------------------------------------
    total_invoiced_tvac_CP_web = fields.Monetary(compute='_compute_total_invoiced_tvac_cp_web',
                                                 string='Total facturé CP pour le web',
                                                 required=False)
    budget_restant_CP_web = fields.Monetary(compute='_compute_budget_restant_CP_web',
                                            string='Budget restant CP pour le web',
                                            required=False)

    # CCartouche     ###################################################################################################

   # budget_cartouche = fields.Monetary(string='Budget cartouche',
    #                                   required=False)             # Champs temporaire à faire disparaître
    budget_CC = fields.Monetary(string='Budget Cartouche', required=False)
    total_invoiced_tvac_CC = fields.Monetary(compute='_invoice_total_tvac_CC',
                                             string='Total facturé sur Crédit Cartouche',
                                             required=False)
    budget_restant_CC = fields.Monetary(compute='_compute_budget_restant_CC',
                                        string="Budget restant pour les Cartouches",
                                        required=False)

    # CEconomat   ######################################################################################################

    budget_CE = fields.Monetary(string='Budget Economat', required=False)
    total_invoiced_tvac_CE = fields.Monetary(compute='_invoice_total_tvac_CE', string="Total Invoiced CE", required=False)
    budget_restant_CE = fields.Monetary(compute='_compute_budget_restant_CE',
                                        string="Budget restant sur Crédit Economat")

        # Champs pour l'exposition sur le site Web -------------------------------------------------
    budget_CE_web = fields.Monetary(compute='_compute_budget_CE_web',
                                    string='Budget économat pour web')
    budget_restant_CE_web = fields.Monetary(compute='_compute_budget_restant_CE_web',
                                            string='Budget restant CE pour le web',
                                            store=False)
    total_invoiced_tvac_CE_web = fields.Char(compute='_compute_total_invoiced_tvac_CE_web',
                                                 string='Total facturé CE pour le web',
                                                 store=False)
    total_invoiced_tvac_CE_web_test = fields.Monetary(compute='_compute_total_invoiced_tvac_CE_web_test',
                                                      string='Total facturé CE pour le web test',
                                                      store=False)



    # TOTAL_INVOICED_TVAC : Calcul du total des factures TVAC (tous budgets confondus et année en cours)

    @api.multi
    def _invoice_total_tvac(self):
        account_invoice = self.env['account.invoice']
        if not self.ids:
            self.total_invoiced_tvac = 0.0
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


    # ______________________________________________________________________________________________#
    # TOTAL_INVOICED_TVAC_CP : Calcul du total des factures TVAC sur le budget "CREDIT PROPRE"   #
    # ---------------------------------------------------------------------------------------------#

    @api.multi
    def _invoice_total_tvac_CP(self):
        account_invoice = self.env['account.invoice']
        if not self.ids:
            self.total_invoiced_tvac_CP = 0.0
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

        where_query = account_invoice._where_calc([
            ('partner_id', 'in', all_partner_ids), ('state', 'not in', ['draft', 'cancel']),
            ('type', 'in', ('out_invoice', 'out_refund')), ('date', '>=', today),
            ('payment_acquirer_id_budget', '=', 'Credit Papier')
        ])
        # Wire Transfer : on défini un nom à l'intermédiaire de paiement dans l'interface et on filtrer sur ce nom
        account_invoice._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        query = """
              SELECT SUM(amount_total_signed) as total, partner_id
                FROM account_invoice account_invoice
               WHERE %s
               GROUP BY partner_id
            """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            partner.total_invoiced_tvac_CP = sum(price['total']
                                              for price in price_totals if price['partner_id'] in child_ids)

    # Calcul du budget restant qui est la différence entre le budget donné et la somme des factures de l'année en
    # cours TVAC pour le budget "Crédit Economat"


#############################################################################################
########################          Calculs sur Crédit Papier     #############################

    @api.multi
    @api.depends('total_invoiced_tvac_CP')
    def _compute_total_invoiced_tvac_cp_web(self):
        for partner in self:
            partner.total_invoiced_tvac_CP_web = partner.total_invoiced_tvac_CP

    @api.depends('total_invoiced_tvac_CP', 'budget_CP')
    def _compute_budget_restant_CP(self):
            for partner in self:
                partner.budget_restant_CP = partner.budget_CP - partner.total_invoiced_tvac_CP


    @api.onchange('budget_restant_CP')
    def _compute_budget_restant_CP_web(self):
        for partner in self:
            partner.budget_restant_CP_web = partner.budget_restant_CP

  ###########################################################################################################
  ##          Pour afficher le budget initial sur le web
  ###########################################################################################################

    @api.multi
    @api.depends('budget_CE')
    def _compute_budget_CE_web(self):
            for partner in self:
                partner.budget_CE_web = partner.budget_CE

    #############################################################################################################
    ##          Pour afficher la somme des achats sur le site web @@@@@@@@@@@@@@@@@@@@@@
    ###########################################################################################################""
    @api.multi
    @api.depends('total_invoiced_tvac_CE')
    def _compute_total_invoiced_tvac_CE_web(self):
            for partner in self:
                partner.total_invoiced_tvac_CE
                partner.total_invoiced_tvac_CE_web = "{mon_champs} papa".format(mon_champs=partner.total_invoiced_tvac_CE)

    @api.multi
    def _compute_total_invoiced_tvac_CE_web_test(self):
            account_invoice = self.env['account.invoice']
            if not self.ids:
                self.total_invoiced_tvac_CE_web_test = 0.1
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

            where_query = account_invoice._where_calc([
                ('partner_id', 'in', all_partner_ids), ('state', 'not in', ['draft', 'cancel']),
                ('type', 'in', ('out_invoice', 'out_refund')), ('date', '>=', today),
                ('payment_acquirer_id_budget', '=', 'Credit Economat')
            ])
            # Credir Economat : on défini un nom à l'intermédiaire de paiement dans l'interface et on filtrer sur
            # ce nom.

            account_invoice._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()

            query = """
                                    SELECT SUM(amount_total_signed) as total, partner_id
                                    FROM account_invoice account_invoice
                                    WHERE %s
                                    GROUP BY partner_id
                                """ % where_clause
            self.env.cr.execute(query, where_clause_params)
            price_totals = self.env.cr.dictfetchall()
            for partner, child_ids in all_partners_and_children.items():
                _logger.warning(u"JE PASSE DANS MA FONCTION DE CALCUL WEB TEST")
                partner.total_invoiced_tvac_CE_web_test = sum(price['total']
                                                     for price in price_totals if price['partner_id'] in child_ids)

            _logger.warning(u"PARAMETRE DU QUERY DE LA PAGE WEB {TOTAL_FACTURES_web}".format(TOTAL_FACTURES_web=where_clause_params))
            _logger.warning(u"Liste des partenaires pour calcul factures web {partners}".format(
                partners=all_partner_ids))
            _logger.warning(u"Montant de price_totals {price_totals}".format(
                price_totals=price_totals))
            _logger.warning(u"VALEUR du INVOICE TVA CE TOTAL {price}".format(
                price=partner.total_invoiced_tvac_CE_web_test))
  #############################################################################################################
  ##          Pour afficher le reste du budget sur le web
  ###########################################################################################################""
    @api.multi
    @api.depends('budget_CE','total_invoiced_tvac_CE_web_test','budget_restant_CE')
    def _compute_budget_restant_CE_web(self):
            for partner in self:
                partner.budget_restant_CE_web = partner.budget_restant_CE
                _logger.warning(u"BUDGET RESTANT CE WEB {BUDGET_RESTANT_CE_web}".format(BUDGET_RESTANT_CE_web=partner.budget_restant_CE_web))

            # ______________________________________________________________________________________________#
            # TOTAL_INVOICED_TVAC_CE : Calcul du total des factures TVAC sur le budget "CREDIT ECONOMAT"   #
            # ---------------------------------------------------------------------------------------------#

    @api.multi
    def _invoice_total_tvac_CE(self):
        account_invoice = self.env['account.invoice']
        if not self.ids:
            self.total_invoiced_tvac_CE = 0.0
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

        where_query = account_invoice._where_calc([
            ('partner_id', 'in', all_partner_ids), ('state', 'not in', ['draft', 'cancel']),
            ('type', 'in', ('out_invoice', 'out_refund')), ('date', '>=', today),
            ('payment_acquirer_id_budget', '=', 'Credit Economat')
        ])
        # Credir Economat : on défini un nom à l'intermédiaire de paiement dans l'interface et on filtrer sur
        # ce nom.

        account_invoice._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        query = """
                        SELECT SUM(amount_total_signed) as total, partner_id
                        FROM account_invoice account_invoice
                        WHERE %s
                        GROUP BY partner_id
                    """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            partner.total_invoiced_tvac_CE = sum(price['total']
                                              for price in price_totals if price['partner_id'] in child_ids)
            _logger.warning(u"SOMME DES FACTURES BACKOFFICE {TOTAL_FACTURES_BACKOFFICE}".format(TOTAL_FACTURES_BACKOFFICE=price_totals))

    # Calcul du budget restant qui est la différence entre le budget donné et la somme des factures de
    # l'année en cours TVAC pour le budget "Crédit Economat".



    @api.one
    @api.onchange('total_invoiced_tvac_CE', 'budget_CE')
    def _compute_budget_restant_CE(self):
        for partner in self:
            partner.budget_restant_CE = partner.budget_CE - partner.total_invoiced_tvac_CE



    ################################################################################################
    ########################          Calculs sur Crédit Cartouche     #############################


    #   Calcul de la somme des factures sur Crédit Cartouche
    @api.multi
    def _invoice_total_tvac_CC(self):
        account_invoice = self.env['account.invoice']
        if not self.ids:
            self.total_invoiced_tvac_CC = 0.0
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

        where_query = account_invoice._where_calc([
            ('partner_id', 'in', all_partner_ids), ('state', 'not in', ['draft', 'cancel']),
            ('type', 'in', ('out_invoice', 'out_refund')), ('date', '>=', today),
            ('payment_acquirer_id_budget', '=', 'Credit Cartouche')
        ])
        # Wire Transfer : on défini un nom à l'intermédiaire de paiement dans l'interface et on filtrer sur ce nom
        account_invoice._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        query = """
              SELECT SUM(amount_total_signed) as total, partner_id
                FROM account_invoice account_invoice
               WHERE %s
               GROUP BY partner_id
            """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            partner.total_invoiced_tvac_CC = sum(price['total']
                                              for price in price_totals if price['partner_id'] in child_ids)


        #   Calcul du solde restant sur le budget Cartouche
    @api.one
    @api.onchange('total_invoiced_tvac_CC', 'budget_CC')
    def _compute_budget_restant_CC(self):
        for partner in self:
            partner.budget_restant_CC = partner.budget_CC - partner.total_invoiced_tvac_CC