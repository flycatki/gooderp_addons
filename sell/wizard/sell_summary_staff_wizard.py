# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError


class sell_summary_staff_wizard(models.TransientModel):
    _name = 'sell.summary.staff.wizard'
    _description = u'销售汇总表（按销售人员）向导'

    @api.model
    def _default_date_start(self):
        return self.env.user.company_id.start_date

    @api.model
    def _default_date_end(self):
        return date.today()

    date_start = fields.Date(u'开始日期', default=_default_date_start,
                             help=u'报表汇总的开始日期，默认为公司启用日期')
    date_end = fields.Date(u'结束日期', default=_default_date_end,
                           help=u'报表汇总的结束日期，默认为当前日期')
    staff_id = fields.Many2one('staff', u'销售人员',
                               help=u'按指定销售员进行统计')
    goods_id = fields.Many2one('goods', u'商品',
                               help=u'按指定商品进行统计')
    goods_categ_id = fields.Many2one('core.category', u'商品类别',
                                     domain=[('type', '=', 'goods')],
                                     context={'type': 'goods'},
                                     help=u'按指定商品类别进行统计')
    warehouse_id = fields.Many2one('warehouse', u'仓库',
                                   help=u'按指定仓库进行统计')

    @api.multi
    def button_ok(self):
        self.ensure_one()
        if self.date_end < self.date_start:
            raise UserError(u'开始日期不能大于结束日期！')
        read_fields = ['date_start', 'date_end', 'staff_id',
                       'goods_id', 'goods_categ_id', 'warehouse_id']
        return {
            'name': u'销售汇总表（按销售人员）',
            'view_mode': 'tree',
            'res_model': 'sell.summary.staff',
            'type': 'ir.actions.act_window',
            'context': self.read(read_fields)[0],
            'limit': 65535,
        }
