#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os

from rapidsms.apps.base import AppBase

class App(AppBase):
    """
    What
    """

    def start(self):
        pass

    def ajax_GET_templates(self, get):
        templates = {}
        # find all the running apps
        for app in self.router.apps:
            msg_dir = app.messages_directory
            app_templates = []
            for (dirpath, dirname, filenames) in os.walk(msg_dir):
                # add files within app's messages directory to list
                # NOTE this will add any included directories too
                app_templates.extend(filenames)
                break
            if app_templates:
                # build list of full paths to each template file
                app_templates_paths = [os.path.join(dirpath, template).replace('/', '-') for template in app_templates]
                # build list of template names (i.e., ignore file extension)
                app_templates_names = [template.split('.')[0] for template in app_templates]
                # add list of (template_file_path, template_name) to templates dict
                templates.update({app.name: zip(app_templates_paths, app_templates_names)})
        return templates

