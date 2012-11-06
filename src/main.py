#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 smallevilbeast
#
# Author:     smallevilbeast <houshao55@gmail.com>
# Maintainer: smallevilbeast <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dtk.ui.thread_pool import MissionThreadPool, MissionThread

import utils

from xdg import get_cache_file
from posterlib import Poster
image_poster = Poster()


def get_save_file(name):
    return get_cache_file("app/%s" % name)

class FetchImage(MissionThread):
    
    def __init__(self, name):
        MissionThread.__init__(self)
        self.app_name = name
        
    def start_mission(self):    
        image_uri = image_poster.query_image(self.app_name)
        if image_uri:
            utils.download(image_uri, get_save_file(self.app_name))
        
            
if __name__ == "__main__":            
    import gtk
    gtk.gdk.threads_init()
    app_list = "amarok chromium chrome exaile emacs".split()
    image_missions_pool = MissionThreadPool(5, exit_when_finish=True)
    if app_list:
        image_missions_pool.add_missions([FetchImage(app_name) for app_name in app_list])
    image_missions_pool.start()    
    gtk.main()

    
    