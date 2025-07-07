# poster.py

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
HASHNODE_API_KEY = os.getenv("HASHNODE_API_KEY")
HASHNODE_PUBLICATION_ID = os.getenv("HASHNODE_PUBLICATION_ID")

print("🔑 DEVTO_API_KEY present:", bool(DEVTO_API_KEY))
print("🔑 HASHNODE_API_KEY present:", bool(HASHNODE_API_KEY))
print("🔑 HASHNODE_PUBLICATION_ID present:", bool(HASHNODE_PUBLICATION_ID))


def post_to_devto(title, content, tags=None, publish=False):
    print("🚀 post_to_devto() function CALLED")
    print("📬 Received title:", title)
    print("📜 Received content length:", len(content))
    print("🏷️ Received tags:", tags)
    print("🟢 Publish status:", publish)
    if not DEVTO_API_KEY:
        raise Exception("❌ DEVTO_API_KEY is missing in .env")

    headers = {
        "api-key": DEVTO_API_KEY,
        "Content-Type": "application/json"
    }

    # Append timestamp to avoid Dev.to duplicate title error
    timestamped_title = f"{title} - {int(time.time())}"

    article_data = {
        "article": {
            "title": timestamped_title,
            "published": publish,
            "body_markdown": content,
            "tags": tags or [],
        }
    }

    print("📡 Posting to Dev.to with the following payload:")
    print(article_data)

    response = requests.post("https://dev.to/api/articles", headers=headers, json=article_data)
    print("📤 Request sent to Dev.to")

    print("🔍 Response status:", response.status_code)
    print("🔍 Response body:", response.text)

    if response.status_code == 201:
        return response.json()["url"]
    else:
        raise Exception(f"❌ Failed to post to Dev.to. Status: {response.status_code}. Response: {response.text}. Check if the content or title is empty or improperly formatted.")


def post_to_hashnode(title, content, tags=None, publish=True):
    print("🚀 post_to_hashnode() function CALLED")
    print("📬 Received title:", title)
    print("📜 Received content length:", len(content))
    print("🏷️ Tags:", tags)

    if not HASHNODE_API_KEY or not HASHNODE_PUBLICATION_ID:
        raise Exception("❌ HASHNODE_API_KEY or HASHNODE_PUBLICATION_ID is missing in .env")

    headers = {
        "Content-Type": "application/json",
        "Authorization": HASHNODE_API_KEY
    }

    # 🔁 Use publishPost mutation (not createDraft)
    query = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          slug
        }
      }
    }
    """

    tag_objects = [{"name": tag, "slug": tag.lower().replace(" ", "-")} for tag in tags] if tags else []

    variables = {
        "input": {
            "title": title.strip(),
            "contentMarkdown": content.strip(),
            "tags": tag_objects,
            "publicationId": HASHNODE_PUBLICATION_ID
        }
    }

    print("📡 Sending to Hashnode:")
    print(variables)

    response = requests.post(
        "https://gql.hashnode.com",
        headers=headers,
        json={"query": query, "variables": variables}
    )

    print("🔍 Response status:", response.status_code)
    print("🔍 Response body:", response.text)

    data = response.json()
    if response.status_code == 200 and "errors" not in data:
        HASHNODE_SUBDOMAIN = os.getenv("HASHNODE_SUBDOMAIN", "your-subdomain")  # e.g., "rishabh"

        ...

        slug = data["data"]["publishPost"]["post"]["slug"]
        return f"https://{HASHNODE_SUBDOMAIN}.hashnode.dev/{slug}"
    else:
        raise Exception(f"❌ Hashnode publish failed: {data}")
    

    # Get your actual subdomain (manually set it here or fetch via API)
HASHNODE_SUBDOMAIN = os.getenv("HASHNODE_SUBDOMAIN", "your-subdomain")  # e.g., "rishabh"

...

