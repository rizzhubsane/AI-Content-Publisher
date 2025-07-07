# 🧠 AI Content Reformatter & Publisher

This is an autonomous AI agent that takes a single "master article" and automatically:

- ✅ Reformats it for selected platforms (like Dev.to, Hashnode)
- 📝 Generates custom platform-optimized titles and tags using Groq's LLaMA 3 (8B)
- 🚀 Posts the content live via official APIs
- 🔗 Returns links to your published posts

Built with:
- 🐍 Python + Streamlit (UI)
- ⚡ Groq API + LLaMA3 8B (for AI-generated content)
- 🔗 Dev.to REST API
- 🔧 Hashnode GraphQL API
- 🔐 `.env`-based config for secure key handling

## 🚀 Features

- One-click publishing to multiple platforms
- Platform-specific tone and formatting
- Autonomous title + tag generation
- Live publishing (not just drafts)
- Clean, extendable modular structure

## 🌐 Roadmap

- [x] Dev.to and Hashnode integration
- [x] Autonomous tag + title generation
- [x] Live post publishing
- [ ] Substack + Medium integration
- [ ] X/Twitter thread generation
- [ ] Analytics + engagement tracker
- [ ] Post scheduler

## 📁 Repo Structure

📦 content-reformatter
├── main.py               # Streamlit app
├── reformatter.py        # AI logic for rewriting + tag/title generation
├── poster.py             # Platform-specific posting functions
├── prompts.py            # Platform-specific formatting prompts
├── .env                  # API keys (excluded from repo)
└── requirements.txt      # Python dependencies

## 🛠️ Setup

```bash
git clone https://github.com/your-username/content-reformatter.git
cd content-reformatter
pip install -r requirements.txt
touch .env  # Add your keys (GROQ_API_KEY, DEVTO_API_KEY, HASHNODE_API_KEY, HASHNODE_PUBLICATION_ID, HASHNODE_SUBDOMAIN)
streamlit run main.py

🙋‍♂️ Author

Made with ❤️ by @rizzhub — feel free to fork, improve, and use!

Let me know if you'd like a clean logo/preview image to add to the repo or want a license or GitHub Actions badge included.
