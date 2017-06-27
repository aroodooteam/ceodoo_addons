# -*- coding: utf-8 -*-

import logging
import openerp
import openerp.modules.registry
from openerp.modules import get_module_resource
from openerp.tools.translate import _
from openerp import http

from openerp.http import request, serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)


##
## Web Controllers
##

# class Main(http.Controller):
#
#     @http.route('/data_import', type='http', auth="none")
#     def index(self, s_action=None, db=None, **kw):
#         return http.local_redirect('/web', query=request.params, keep_hash=True)
#
#     @http.route([
#         '/data_import/<xmlid>',
#         '/data_import/<xmlid>/<version>',
#     ], type='json', auth="user")
#     def load_needaction(self, menu_ids):
#         """ Loads needaction counters for specific menu ids.
#
#             :return: needaction data
#             :rtype: dict(menu_id: {'needaction_enabled': boolean, 'needaction_counter': int})
#         """
#         return request.session.model('ir.ui.menu').get_needaction_data(menu_ids, request.context)
#
