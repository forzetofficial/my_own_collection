#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Your Name <your.email@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Creates a text file on remote host
version_added: "1.0.0"
description:
    - This module creates a text file on the remote host with specified content.
    - It can create directories if they don't exist.
options:
    path:
        description:
            - Path to the file to create.
        required: true
        type: str
    content:
        description:
            - Content to write to the file.
        required: true
        type: str
    mode:
        description:
            - Permissions of the file (in octal).
        required: false
        type: str
        default: '0644'
author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create a file with content
  my_own_namespace.my_own_collection.my_own_module:
    path: /tmp/example.txt
    content: "Hello, World!"

- name: Create a file with custom permissions
  my_own_namespace.my_own_collection.my_own_module:
    path: /tmp/example.txt
    content: "Hello, World!"
    mode: '0755'
'''

RETURN = r'''
path:
    description: Path to the file that was created/modified
    type: str
    returned: always
    sample: '/tmp/example.txt'
content:
    description: Content that was written to the file
    type: str
    returned: always
    sample: 'Hello, World!'
changed:
    description: Whether the file was changed
    type: bool
    returned: always
    sample: true
'''

import os
import os.path
from ansible.module_utils.basic import AnsibleModule


def run_module():
    # Define module arguments
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        mode=dict(type='str', required=False, default='0644')
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    mode = module.params['mode']

    # Check if file exists and content matches
    file_exists = os.path.exists(path)
    current_content = None

    if file_exists:
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except Exception as e:
            module.fail_json(msg="Failed to read existing file: %s" % str(e), **result)

    # Determine if changes are needed
    if not file_exists or current_content != content:
        if module.check_mode:
            result['changed'] = True
            module.exit_json(**result)
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, mode=0o755)
            except Exception as e:
                module.fail_json(msg="Failed to create directory: %s" % str(e), **result)
        
        # Write file
        try:
            with open(path, 'w') as f:
                f.write(content)
            os.chmod(path, int(mode, 8))
            result['changed'] = True
        except Exception as e:
            module.fail_json(msg="Failed to write file: %s" % str(e), **result)
    
    result['path'] = path
    result['content'] = content
    
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
