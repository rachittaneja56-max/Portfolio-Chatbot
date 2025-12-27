def classify_domains(question: str) -> list[str]:
    q = question.lower()

    domain_keywords = {
        "about": ["about", "background", "intro", "who", "focus", "summary"],
        "skills": ["skill", "skills", "technology", "tech", "stack", "tools"],
        "projects": ["project", "projects", "built", "work", "portfolio"],
        "certifications": ["certificate", "certification", "course", "program"],
        "blog": ["blog", "write", "writing", "posts"],
        "contact": ["contact", "email", "github", "linkedin", "reach"]
    }

    matched_domains = []

    for domain, keywords in domain_keywords.items():
        if any(keyword in q for keyword in keywords):
            matched_domains.append(domain)

    return matched_domains
