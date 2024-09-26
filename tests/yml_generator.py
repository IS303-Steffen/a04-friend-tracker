import os
from ruamel.yaml import YAML

def generate_classroom_yml(python_version='3.12'):
    # Initialize ruamel.yaml YAML instance
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 1000  # Prevent line breaks in long strings

    # Define the structure of the YAML file using regular dictionaries
    data = {}
    data['name'] = 'Autograding Tests'
    data['on'] = ['push', 'repository_dispatch']
    data['permissions'] = {
        'checks': 'write',
        'actions': 'read',
        'contents': 'read'
    }
    data['jobs'] = {}
    data['jobs']['run-autograding-tests'] = {}
    job = data['jobs']['run-autograding-tests']
    job['runs-on'] = 'ubuntu-latest'
    job['if'] = "github.actor != 'github-classroom[bot]'"
    job['steps'] = []

    # Add initial steps
    job['steps'].append({
        'name': 'Checkout code',
        'uses': 'actions/checkout@v4'
    })
    job['steps'].append({
        'name': 'Set up Python',
        'uses': 'actions/setup-python@v3',
        'with': {'python-version': python_version}
    })

    # Add install dependencies step
    job['steps'].append({
        'name': 'Install dependencies',
        'run': 'python -m pip install --upgrade pip && pip install pandas openpyxl pytest pytest-subtests \'black<=22.3.0\' \'tomli>=1.1.0\' \'timeout-decorator~=0.5.0\''
    })

    # Add test steps dynamically based on the test_*.py files in the tests/ folder
    test_files = [f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]

    # Sort the test files by the number in the filename to ensure they are in order
    test_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    test_names = []
    for test_file in test_files:
        test_name = test_file.replace('.py', '').replace('_', '-')
        test_names.append(test_name)
        
        # Use autograding-command-grader instead of autograding-python-grader
        job['steps'].append({
            'name': f'tests/{test_file}',
            'id': f'tests-{test_name}-py',
            'uses': 'classroom-resources/autograding-command-grader@v1',
            'with': {
                'test-name': f'{test_name}',
                'setup-command': '',
                'command': f'python -m pytest -v tests/{test_file}',
                'timeout': 10,
                'max-score': 15  # Adjust max-score as needed
            }
        })

    # Ensure the .github/workflows directory exists
    os.makedirs('.github/workflows', exist_ok=True)

    # Write the YAML data to the classroom.yml file
    with open('.github/workflows/classroom.yml', 'w') as file:
        yaml.dump(data, file)

if __name__ == '__main__':
    # Call the function with a default or custom Python version
    generate_classroom_yml()