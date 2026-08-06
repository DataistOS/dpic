import os
import json
import re

def convert_plan_rst_to_json():
    """Converts the plan.rst file containing business plans and services into a structured JSON file using the Docs as Code approach.

    This function reads the `plan.rst` file from the project's source directory, 
    extracts footnotes and tabular data (`list-table`), structures them into 
    a Python dictionary, and saves the result as `plan.json` inside `_templates/docs_as_code`.
    """
    # Define relative paths based on the project structure
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    
    # Define input (plan.rst) path
    models_dir = os.path.join(project_root, '_source', 'category', 'economy', 'business', 'models')
    rst_path = os.path.join(models_dir, 'plan.rst')

    # Define output (plan.json) path in _templates/docs_as_code directory
    templates_dir = os.path.join(project_root, '_templates', 'docs_as_code')
    os.makedirs(templates_dir, exist_ok=True)
    json_path = os.path.join(templates_dir, 'plan.json')

    if not os.path.exists(rst_path):
        print(f"Error: فایل {rst_path} پیدا نشد!")
        return

    with open(rst_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract footnotes from the end of the file
    footnotes = {}
    lines = content.split('\n')
    current_fn = None
    fn_text = []
    
    for line in lines:
        fn_match = re.match(r'^\.\.\s+\[#([a-zA-Z0-9_-]+)\]\s+(.*)', line)
        if fn_match:
            if current_fn:
                footnotes[current_fn] = " ".join(fn_text).strip()
            current_fn = fn_match.group(1)
            fn_text = [fn_match.group(2)]
        elif current_fn and line.startswith('   '):
            fn_text.append(line.strip())
        elif current_fn and line.strip() == '':
            if current_fn:
                footnotes[current_fn] = " ".join(fn_text).strip()
                current_fn = None
                fn_text = []
    if current_fn:
        footnotes[current_fn] = " ".join(fn_text).strip()

    # Extract table data (list-table)
    table_start = content.find('.. list-table::')
    if table_start == -1:
        print("Error: بلوک list-table در فایل plan.rst پیدا نشد!")
        return

    table_content = content[table_start:]
    role_blocks = re.split(r'\n\s+\*\s+-\s+(\d+)\s*\n', table_content)
    
    roles_data = []
    for i in range(1, len(role_blocks), 2):
        code = role_blocks[i].strip()
        block_text = role_blocks[i+1]
        
        lines_in_block = [l.strip() for l in block_text.split('\n') if l.strip()]
        if len(lines_in_block) < 2:
            continue
            
        eng_name = lines_in_block[0]
        title_fa = lines_in_block[1]
     
        roles_data.append({
            "code": int(code),
            "name": eng_name,
            "title": title_fa,
            "raw_block": block_text
        })

    output_data = {
        "metadata": {
            "title": "ماتریس خدمات و طرح‌های درآمدی اکوسیستم داده‌گرا",
            "source_file": "plan.rst"
        },
        "roles": roles_data,
        "footnotes": footnotes
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
     
    print(f"Success: فایل plan.json با موفقیت در {json_path} ذخیره شد.")

if __name__ == '__main__':
    convert_plan_rst_to_json()
