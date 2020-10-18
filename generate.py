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

#   /*
#   
#   returns the path to all of the .rst files in given directory
#
#   args:
#       folder_path: the path to the directory which contains the .rst files
#   
#   returns:
#       - path to given .rst file
#       - .rst filename
#   
#   */
def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        # ignore non-.rst files
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name), base

#   /*
#   
#   json-ify a .rst file. content is metadata['content']
#
#   args:
#       file_path: the path to the target .rst file
#   
#   returns:
#       - json object
#   
#   */
def read_file(file_path):
    with open(file_path, 'r') as f:
        raw_metadata = ""

        # metadata
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line

        # content
        content = ""
        for line in f:
            content += line 

        metadata = json.loads(raw_metadata)
        if len(metadata) == 0:
            metadata = None
        else:
            # get rid of stray \n
            metadata['content'] = content.strip()

    return metadata

#   /*
#   
#   writes the actual output .html files
#
#   args:
#       - name: name of file without extension
#       - html: content of file
#       - output_dir: path to output directory
#   
#   */
def write_output(name, html, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open(os.path.join(output_dir, name + ".html"), 'w') as f:
        f.write(html)

#   /*
#   
#   initializes jinja2 environment. renders the html contents of each file,
#   finally calls write_output() with the rendered html content
#
#   args:
#       - folder_path: path to source files
#       - output_dir: path to output directory
#   
#   */
def generate_site(folder_path, output_dir):
    log.info("Generating site from %r", folder_path)
    # initialize jinja2 environment & loader
    jinja_loader = jinja2.FileSystemLoader(os.path.join(folder_path, 'layout'))
    jinja_env = jinja2.Environment(loader = jinja_loader, trim_blocks = True, lstrip_blocks = True)

    for file_path, name in list_files(folder_path):
        metadata = read_file(file_path)
        if metadata == None:
            # skip this file if no metadata provided
            continue
        try:
            # don't get template name if it doesn't exist (assigning as None would not throw TemplateNotFound for some reason)
            template_name = metadata['layout'] if len(metadata) > 2 else ""
            template = jinja_env.get_template(template_name)
        except jinja2.exceptions.TemplateNotFound:
            # skip this file if can't find the template for it
            continue

        html = template.render(metadata)

        # get rid of excess new lines.
        # alternatively could have added `-` for the template content block
        html = html.replace('\n\n', '\n')
        write_output(name, html, output_dir)
        log.info("Writing %r with template %r", name, template_name)


def main(input_dir, output_dir):
    generate_site(input_dir, output_dir)


if __name__ == '__main__':
    logging.basicConfig()
    # break out if wrong usage
    if len(sys.argv) != 3:
        raise TypeError("Unexpected number of arguments. Exiting...")

    main(sys.argv[1], sys.argv[2])
