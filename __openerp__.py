# -*- coding: utf-8 -*-
{
    'name': "Stock VDL",

    'summary': """
        Extention du module Stock Picking pour pouvoir laisser un commentaire sur la picking list des magasiniers.""",

    'description': """
        Le module modifie juste le module stock picking et l'information doit être encodé directement sur la picking list mais il n'est pas encore possible de l'encoder 
        via la rédaction du bon de commande (sale_order).

    """,

    'author': "Roland Neyrinck",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_stock', 'sale', 'purchase', 'stock'],

    'data': ['views/magasin_views.xml'
             'Bon_economat.xml'
             ],

}