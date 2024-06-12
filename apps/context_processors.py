def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = "https://"
    else:
        scheme = "http://"

    base_url = f"{scheme}{request.get_host()}"
    try:
        port = request.META.get("HTTP_REFERER").split(":")[2].split("/")[0]
        if port != 80:
            base_url = f"{scheme}{request.get_host()}:{port}"
    except Exception as ex:
        pass
    return {
        "BASE_URL": base_url,
    }
