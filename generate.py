# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import sys
import json
import logging
import jinja2

log = logging.getLogger(__name__)


def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name), base

def read_file(file_path):
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            line = line.rstrip("\n")
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            line = line.rstrip("\n")
            content += line
    return json.loads(raw_metadata), content

def write_output(name, html, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open(os.path.join(output_dir, name + ".html"), 'w') as f:
        f.write(html)

def generate_site(folder_path, output_dir):
    log.info("Generating site from %r", folder_path)
    jinja_loader = jinja2.FileSystemLoader(os.path.join(folder_path, 'layout'))
    jinja_env = jinja2.Environment(loader = jinja_loader, trim_blocks = True, lstrip_blocks = True)
    for file_path, name in list_files(folder_path):
        metadata, metadata['content'] = read_file(file_path)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        html = template.render(metadata)

        # get rid of excess new lines.
        # alternatively could have added `-` for the template content block
        html = html.replace('\n\n', '\n')
        write_output(name, html, output_dir)
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
