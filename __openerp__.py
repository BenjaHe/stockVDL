# -*- coding: utf-8 -*-
{
    'name': "Stock VDL",

    'summary': """
        Extention du module Stock Picking et Res.Partner pour les besoins de l'Economat.""",

    'description': """
        Le module modifie les modules res.partner et stock pour ajouter un commentaire pour la livraison (Inventaire) 
        et les informations liées au budget du client (Contacts).

    """,

    'author': "Roland Neyrinck",
    'website': "",

    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_stock', 'sale', 'purchase', 'stock', 'account', 'sale_order'],

    'data': ['views/magasin_views.xml',
             'views/report_economat.xml',
             'views/account_total.xml'
             ],

}