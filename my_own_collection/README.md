# My Own Collection

## Modules
### my_own_module
Creates a text file on the remote host with specified content.

#### Parameters
- `path` (required): Path to the file to create
- `content` (required): Content to write to the file
- `mode` (optional): File permissions (default: 0644)

## Roles
### my_own_role
Role that uses my_own_module to create files.

#### Role Variables
- `file_path`: Path to the file (default: /tmp/default_file.txt)
- `file_content`: Content to write (default: "Default content from role")
- `file_mode`: File permissions (default: 0644)

## Usage Example
\`\`\`yaml
- name: Create file using custom module
  my_own_namespace.my_own_collection.my_own_module:
    path: /tmp/example.txt
    content: "Hello, World!"
\`\`\`

## Installation
\`\`\`bash
ansible-galaxy collection install my_own_namespace-my_own_collection-1.0.0.tar.gz
\`\`\`

## License
GNU General Public License v3.0
