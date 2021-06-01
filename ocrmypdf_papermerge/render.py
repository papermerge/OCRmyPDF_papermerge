import os.path
from jinja2 import Environment, FileSystemLoader


def render_to_string(template_name, **context):
    output = ""
    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    templates_dir = os.path.join(
        current_dir,
        "templates"
    )
    _loader = FileSystemLoader(templates_dir)
    _env = Environment(loader=_loader)

    template = _env.get_template(template_name)
    output = template.render(**context)

    return output
