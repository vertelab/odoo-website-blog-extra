# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp import http
from openerp.http import request
from openerp.addons.website_blog.controllers.main import WebsiteBlog
import os

class SimpleBlog(http.Controller):

    @http.route([
                '/blog/<model("blog.blog"):simple_blog>',
                '/blog/<model("blog.blog"):simple_blog>/post/<model("blog.post"):simple_blog_post>'
                ],
                type='http', auth="public", website=True)
    def view_simple_blogs(self, simple_blog=None, simple_blog_post=None, **post):
        simple_blog_list = request.env['blog.post'].sudo().search([('blog_id', '=', simple_blog.id)])
        if simple_blog_post:
            # return request.website.render("website_blog_simple.simple_blog_posts", {'simple_blog': simple_blog, 'simple_blog_list': simple_blog_list, 'simple_blog_post': simple_blog_post})
            return request.website.render("website_blog.blog_post_complete", {'simple_blog': simple_blog, 'simple_blog_list': simple_blog_list, 'simple_blog_post': simple_blog_post})
        return request.website.render("website_blog_simple.simple_blog", {'simple_blog': simple_blog, 'simple_blog_list': simple_blog_list})

class website(models.Model):
    _inherit = 'website'

    def simple_blog_url(self, record, recipe):
        """Returns a local url that points to the image field of a given browse record."""
        if record.image:
            return self.imagemagick_url(record, 'image', recipe)
        if record.author_avatar:
            return self.imagemagick_url(record, 'author_avatar', recipe)
        return '/imageurl/%s/ref/%s' % (os.path.join('web', 'static', 'src', 'img', 'stock_person.png'), recipe)

class BlogPost(models.Model):
    _inherit = "blog.post"

    image = fields.Binary(string="Image")
