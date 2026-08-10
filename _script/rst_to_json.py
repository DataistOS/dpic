import os
import json
import re

def convert_plan_rst_to_json():
    """Parses business plan documentation from RST to JSON and generates Dart service code.

    Reads 'plan.rst' from the models directory, extracts service roles and metadata,
    serializes them into 'plan.json', and triggers the generation of the
    'AccessMatrixService' Dart class.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))

    models_dir = os.path.join(project_root, '_source', 'category', 'economy', 'business', 'models')
    rst_path = os.path.join(models_dir, 'plan.rst')

    templates_dir = os.path.join(project_root, '_templates', 'docs_as_code')
    os.makedirs(templates_dir, exist_ok=True)
    json_path = os.path.join(templates_dir, 'plan.json')
    dart_path = os.path.join(templates_dir, 'access_matrix_service.dart')

    if not os.path.exists(rst_path):
        print(f"Error: Could not find {rst_path}")
        return

    with open(rst_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extracts footnotes from the RST content.
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

    # Parses the list-table block from RST.
    table_start = content.find('.. list-table::')
    if table_start == -1:
        print("Error: Could not find list-table block in plan.rst")
        return

    table_content = content[table_start:]
    role_blocks = re.split(r'\n\s+\*\s+-\s+(\d+)\s*\n', table_content)

    roles_data = []
    service_metadata_map = {}

    for i in range(1, len(role_blocks), 2):
        code = role_blocks[i].strip()
        block_text = role_blocks[i+1]

        lines_in_block = [l.strip() for l in block_text.split('\n') if l.strip()]
        if len(lines_in_block) < 2:
            continue

        eng_name = re.sub(r'^-\s*', '', lines_in_block[0]).strip()
        title_fa = re.sub(r'^-\s*', '', lines_in_block[1]).strip()

        roles_data.append({
            "code": int(code),
            "name": eng_name,
            "title": title_fa,
            "raw_block": block_text
        })

        # Extracts URL if present in the block.
        url_match = re.search(r'https?://[^\s]+', block_text)
        link = url_match.group(0) if url_match else ""

        service_metadata_map[title_fa] = {
            "desc": title_fa,
            "link": link
        }

    output_data = {
        "metadata": {
            "title": "Data-driven Ecosystem Business Plan Matrix",
            "source_file": "plan.rst"
        },
        "roles": roles_data,
        "service_metadata": service_metadata_map,
        "footnotes": footnotes
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Success: JSON data generated at {json_path}")
    generate_dart_from_json(json_path, dart_path)

def generate_dart_from_json(json_path, dart_path):
    """Generates the AccessMatrixService Dart class from JSON data.

    Args:
        json_path: Path to the source JSON file.
        dart_path: Destination path for the generated Dart file.
    """

    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    roles_data = data.get("roles", [])
    service_metadata_map = data.get("service_metadata", {})

    metadata_lines = []
    for title, info in service_metadata_map.items():
        escaped_title = title.replace('"', '\\"')
        escaped_desc = info["desc"].replace('"', '\\"')
        escaped_link = info["link"].replace('"', '\\"')

        metadata_lines.append(f'''    "{escaped_title}": {{
      "desc": "{escaped_desc}",
      "link": "{escaped_link}",
    }},''')

    metadata_str = "\n".join(metadata_lines)

    # Logic categorization for service mapping.
    legal_free, legal_bronze, legal_silver, legal_gold = [], [], [], []
    individual_free, individual_bronze, individual_silver, individual_gold = [], [], [], []
    malek_free, malek_tier = [], []
    other_roles_mapping = {
        'participant': [], 'donation': [], 'investor': [], 'brand': [],
        'advertising': [], 'nextcloud': [], 'dass': [], 'dataist_free': [],
        'dataist_other': [], 'databoss': [], 'staff': []
    }

    for idx, role in enumerate(roles_data):
        title = role['title']

        if idx < 10:
            legal_free.append(title)
            individual_free.append(title)
            malek_free.append(title)
        elif idx < 15:
            legal_bronze.append(title)
            individual_bronze.append(title)
        elif idx < 17:
            legal_silver.append(title)
            individual_silver.append(title)
        elif idx < 20:
            legal_gold.append(title)
            individual_gold.append(title)
        else:
            if 'ملک' in title or 'مالک' in title:
                malek_tier.append(title)
            elif 'ابزار' in title:
                if 'رایگان' in title:
                    other_roles_mapping['dataist_free'].append(title)
                else:
                    other_roles_mapping['dataist_other'].append(title)
            elif 'ابری' in title or 'نکس' in title:
                other_roles_mapping['nextcloud'].append(title)
            elif 'پردازش' in title:
                other_roles_mapping['dass'].append(title)
            elif 'پرسنل' in title or 'مدیریتی' in title:
                other_roles_mapping['staff'].append(title)
            else:
                other_roles_mapping['brand'].append(title)

    dart_content = f"""class AccessMatrixService {{
  static final Map<String, Map<String, String>> serviceMetadata = {{
{metadata_str}
  }};

  static Map<String, String>? getServiceDetails(String serviceName) {{
    return serviceMetadata[serviceName];
  }}

  static List<String> getAvailableServices({{
    required String userType,
    required List<String> roles,
    required String tier,
  }}) {{
    List<String> services = [];

    if (userType == 'legal') {{
      if (tier == 'free') {{
        services.addAll({json.dumps(legal_free, ensure_ascii=False)});
      }} else if (tier == 'bronze') {{
        services.addAll({json.dumps(legal_bronze, ensure_ascii=False)});
      }} else if (tier == 'gold') {{
        services.addAll({json.dumps(legal_gold, ensure_ascii=False)});
      }} else if (tier == 'silver') {{
        services.addAll({json.dumps(legal_silver, ensure_ascii=False)});
      }}
    }} else if (userType == 'individual') {{
      if (tier == 'free') {{
        services.addAll({json.dumps(individual_free, ensure_ascii=False)});
      }} else if (tier == 'bronze') {{
        services.addAll({json.dumps(individual_bronze, ensure_ascii=False)});
      }} else if (tier == 'gold') {{
        services.addAll({json.dumps(individual_gold, ensure_ascii=False)});
      }} else if (tier == 'silver') {{
        services.addAll({json.dumps(individual_silver, ensure_ascii=False)});
      }}
    }}

    if (roles.contains('malek')) {{
      if (tier == 'free') {{
        services.addAll({json.dumps(malek_free, ensure_ascii=False)});
      }} else if (tier == 'gold' || tier == 'silver') {{
        services.addAll({json.dumps(malek_tier, ensure_ascii=False)});
      }}
    }}

    if (roles.contains('participant') || roles.contains('donation')) {{
      services.add("حضور و فعالیت در اکوسیستم به عنوان شریک و همکار");
    }}

    if (roles.contains('investor')) {{
      services.add("تأمین مالی مبتنی بر درآمد (RBF)");
    }}

    if (roles.contains('brand')) {{
      services.add("همکاری تجاری و پروموت برند");
    }}

    if (roles.contains('advertising')) {{
      services.add("کمپین‌های بنری و پروموت هدفمند");
    }}

    if (roles.contains('nextcloud')) {{
      services.addAll({json.dumps(other_roles_mapping['nextcloud'], ensure_ascii=False)});
    }}

    if (roles.contains('dass')) {{
      services.addAll({json.dumps(other_roles_mapping['dass'], ensure_ascii=False)});
    }}

    if (roles.contains('dataist')) {{
      if (tier == 'free') {{
        services.addAll({json.dumps(other_roles_mapping['dataist_free'], ensure_ascii=False)});
      }} else {{
        services.addAll({json.dumps(other_roles_mapping['dataist_other'], ensure_ascii=False)});
      }}
    }}

    if (roles.contains('databoss')) {{
      services.add("ثبت و مدیریت داده‌ها در داده‌سالار (DataBoss)");
    }}

    if (roles.contains('staff')) {{
      services.addAll({json.dumps(other_roles_mapping['staff'], ensure_ascii=False)});
    }}

    return services.toSet().toList();
  }}

  static List<Map<String, dynamic>> getAllServicesWithStatus({{
    required String userType,
    required List<String> roles,
    required String currentTier,
  }}) {{
    const List<String> allPossibleTiers = ['free', 'bronze', 'silver', 'gold'];
    List<Map<String, dynamic>> allServicesWithStatus = [];

    for (var t in allPossibleTiers) {{
      List<String> tierServices = getAvailableServices(
        userType: userType,
        roles: roles,
        tier: t,
      );

      bool isAllowed = _isTierAllowed(currentTier, t);

      for (var service in tierServices) {{
        if (!allServicesWithStatus.any((item) => item['service'] == service)) {{
          allServicesWithStatus.add({{
            'tier': t,
            'service': service,
            'isAllowed': isAllowed,
          }});
        }}
      }}
    }}

    return allServicesWithStatus;
  }}

  static bool _isTierAllowed(String currentTier, String serviceTier) {{
    const tierHierarchy = {{'free': 0, 'bronze': 1, 'silver': 2, 'gold': 3}};
    int currentVal = tierHierarchy[currentTier] ?? 0;
    int serviceVal = tierHierarchy[serviceTier] ?? 0;
    return currentVal >= serviceVal;
  }}
}}
"""

    with open(dart_path, 'w', encoding='utf-8') as f:
        f.write(dart_content)

    print(f"Success: Dart file generated at {dart_path}")

if __name__ == '__main__':
    convert_plan_rst_to_json()
