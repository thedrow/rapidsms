#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from rapidsms.contrib.ajax.exceptions import RouterNotResponding

from . import utils

def message_templates(req):
    try:
        router_available = True
        templates = utils.get_templates()
    except RouterNotResponding:
        router_available = False
        templates = None

    return render_to_response(
        "message_editor/index.html", {
            "templates": templates
        }, context_instance=RequestContext(req)
    )

def edit_template(req, path):
    if req.method == 'POST':
        template_content = req.POST.get('template_content')
        if template_content:
            f = open(path, 'w')
            f.write(template_content)
            f.close()
        return redirect('message_templates')
    path = path.replace('-', '/')
    template_content = open(path, 'r').read()

    return render_to_response(
        "message_editor/edit.html", {
            "template_path": path,
            "template_content": template_content
        }, context_instance=RequestContext(req)
    )

