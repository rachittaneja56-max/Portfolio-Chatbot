def extract_context(portfolio: dict, domains: list[str]) -> dict:
    context = {}

    for domain in domains:
        if domain in portfolio:
            context[domain] = portfolio[domain]

    return context
