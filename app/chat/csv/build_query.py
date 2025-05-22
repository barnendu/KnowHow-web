def build_query(query):
    prompt = f"""For the following query, if it requires drawing a table, reply as follows:
    {{
        "table": {{
            "columns": ["column1", "column2", ...],
            "data": [
                [value1, value2, ...],
                [value1, value2, ...],
                ...
            ]
        }}
    }}
    Otherwise, just provide the text response.
    
    Query: {query}
    """
    return prompt