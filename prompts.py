PLATFORM_PROMPTS = {
    "Dev.to": (
        "You are an expert tech writer familiar with Dev.to. "
        "Reformat the following master article so it fits the tone, markdown, and expectations of a Dev.to post. "
        "Use proper markdown headers, lists, and emphasize key points. Do not add any intro or filler. "
        "Here is the article:\n\n{{MASTER_ARTICLE}}"
    ),
    "Hashnode": (
        "You are a professional developer blogger familiar with Hashnode. "
        "Take the following master article and reformat it into a well-structured blog post optimized for Hashnode. "
        "Use markdown, maintain a personal tone, and preserve all core sections. "
        "Here is the article:\n\n{{MASTER_ARTICLE}}"
    )
}