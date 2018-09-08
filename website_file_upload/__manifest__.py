# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Kinfinity Tech Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website File Upload',
    "summary": "Website File Upload,",
    'version': '11.0.1.0.0',
    'category': 'web',
    "description": """
        This modules offers you to upload file from website.
    """,
    'author': 'Kinfinity Tech Pvt. Ltd.',
    'maintainer': 'Kinfinity Tech Pvt. Ltd.',
    'website': 'http://www.kinfinitytech.com',
    'depends': [
        'website_sale'
    ],
    'data': [
        'views/template.xml',
    ],
    'qweb': [
        # 'static/src/xml/*.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL'
}
