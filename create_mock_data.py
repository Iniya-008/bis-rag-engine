import json
import os

mock_standards = [
    {
        "id": "IS 456",
        "title": "Plain and Reinforced Concrete - Code of Practice",
        "description": "This standard deals with the general structural use of plain and reinforced concrete. It covers specifications for materials, workmanship, inspection, and testing for concrete structures like building columns, beams, and slabs."
    },
    {
        "id": "IS 383",
        "title": "Coarse and Fine Aggregate for Concrete - Specification",
        "description": "This standard prescribes the requirements for coarse and fine aggregates for use in the preparation of concrete. It covers natural and crushed aggregates, including sand and gravel."
    },
    {
        "id": "IS 10262",
        "title": "Concrete Mix Proportioning - Guidelines",
        "description": "This standard provides guidelines for proportioning concrete mixes as per the requirements using the concrete making materials including other supplementary materials identified for this purpose."
    },
    {
        "id": "IS 1786",
        "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement",
        "description": "This standard specifies requirements for high strength deformed steel bars and wires for use as reinforcement in concrete, covering various grades and mechanical properties."
    },
    {
        "id": "IS 269",
        "title": "Ordinary Portland Cement - Specification",
        "description": "This standard covers the manufacture and chemical and physical requirements of ordinary Portland cement. Used extensively for general masonry and concrete work."
    }
]

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    output_path = os.path.join(base_dir, "parsed_standards.json")
    with open(output_path, 'w') as f:
        json.dump(mock_standards, f, indent=4)
    print(f"Generated mock data with {len(mock_standards)} standards at {output_path}")

    # Create input.json for inference
    mock_input = [
        {
            "id": "q1",
            "query": "high strength reinforced concrete for building columns"
        },
        {
            "id": "q2",
            "query": "gravel and fine sand for mixing concrete"
        }
    ]
    input_path = os.path.join(base_dir, "input.json")
    with open(input_path, 'w') as f:
        json.dump(mock_input, f, indent=4)
    print(f"Generated mock input queries at {input_path}")
