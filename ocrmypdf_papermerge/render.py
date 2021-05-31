import os.path
from jinja2 import Template


def render_to_string(template_name, **context):
    output = ""
    current_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    template_path = os.path.join(
        current_dir,
        template_name
    )

    with open(template_path, "rt") as f:
        page_template_j2 = f.read()
        template = Template(page_template_j2)
        output = template.render(**context)

    return output
