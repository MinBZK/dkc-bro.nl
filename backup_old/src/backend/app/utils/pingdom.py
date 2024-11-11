def generate_pingdom_xml(status, code):
    return f"""
    <pingdom_http_custom_check>
        <status>{status}</status>
        <response_time>{code}</response_time>
    </pingdom_http_custom_check>
    """
