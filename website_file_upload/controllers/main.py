# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.ir.ir_qweb.fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression

class WebsiteSaleForm(WebsiteForm):

    @http.route('/quick', type='http',
                auth="public",  website=True)
    def quick_order(self):
        return request.render('website_file_upload.open_file')

    @http.route('/website_form/shop.quick.sale.order', type='http',
                auth="public", methods=['POST'], website=True)
    def website_form_quick_saleorder(self, **kwargs):
        model_record = request.env.ref('sale.model_sale_order')
        order = request.website.sale_get_order()
        try:
            data = self.extract_data(model_record, kwargs)
            import openpyxl
            workbook = openpyxl.load_workbook(data['attachments'][0])
            sheet = workbook.active

            rows = sheet.rows

            values = []
            i = 1
            for row in rows:
                if i > 1:
                    vals = []
                    for cell in row:
                        vals.append(cell.value)
                    values.append(vals)
                i+=1
        except ValidationError as e:
            return json.dumps({'error_fields': e.args[0]})
        ProductObj = request.env['product.product']
        for val in values:
            product_id = ProductObj.search([('default_code', '=', val[0])],
                                         limit=1)
            out_of_stock = []
            if product_id and product_id.qty_available >= val[1]:
                order._cart_update(product_id=product_id.id, line_id=None,
                                   add_qty=float(val[1]), set_qty=None)
            else:
                out_of_stock.append(val[0])
        if data['record']:
            order.write(data['record'])

        if data['custom']:
            values = {
                'body': nl2br(data['custom']),
                'model': 'sale.order',
                'message_type': 'comment',
                'no_auto_thread': False,
                'res_id': order.id,
            }
            request.env['mail.message'].sudo().create(values)

        if data['attachments']:
            self.insert_attachment(model_record, order.id, data['attachments'])

        return json.dumps({'id': order.id})

