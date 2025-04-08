import json

def parse_elementor_request(body_text: str, form_data=None) -> dict:
    """
    Parses incoming Elementor webhook data, either from JSON or form-data.
    Returns cleaned data as a dictionary.
    """
    cleaned_data = {}

    # Try parsing JSON first
    try:
        payload = json.loads(body_text)
        fields = payload.get("fields", {})
        meta = payload.get("meta_data", {})

        # Merge fields and meta data (optional)
        cleaned_data = {**fields, **meta}

    except json.JSONDecodeError:
        # Process form data if JSON parsing fails
        if form_data is None:
            return cleaned_data

        field_values = {}
        field_titles = {}

        for raw_key, value in form_data.items():
            if "][" in raw_key:
                base, prop = raw_key.split("][", 1)
                prop = prop.rstrip("]")

                if prop == "value":
                    field_values[base] = value
                elif prop == "title":
                    field_titles[base] = value

        for field_id, field_value in field_values.items():
            field_title = field_titles.get(field_id, field_id)
            cleaned_data[field_title] = field_value

    return cleaned_data