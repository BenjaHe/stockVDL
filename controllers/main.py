# -*- coding: utf-8 -*-
import datetime

from openerp import http
from openerp.exceptions import AccessError
from openerp.http import request

from openerp.addons.website_portal.controllers.main import website_account


class website_account(website_account):

    @http.route(['/my/home'], type='http', auth="user", website=True)
    def company_details(self, **kw):
        companies = http.request.env['res.company'].sudo().search([])
        return http.request.render("website_portal_sale.orders_followup", {
            'companies': companies})

