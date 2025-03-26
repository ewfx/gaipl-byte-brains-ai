import streamlit as st
from utils.kb_service import KBService
from typing import List, Dict, Any

class KnowledgeBase:
    def __init__(self):
        self.kb_service = KBService()

    def render(self):
        st.header("Knowledge Base")

        # Search bar
        search_query = st.text_input("Search Knowledge Base", "")

        # Create tabs for different KB sections
        tabs = st.tabs(["Articles", "Troubleshooting Guides", "Stack Overflow", "Documentation"])

        with tabs[0]:
            self.render_articles_section(search_query)

        with tabs[1]:
            self.render_troubleshooting_section(search_query)

        with tabs[2]:
            self.render_stack_overflow_section(search_query)

        with tabs[3]:
            self.render_documentation_section(search_query)

    def render_articles_section(self, search_query: str):
        """Render KB articles section"""
        st.subheader("Knowledge Base Articles")

        articles = self.kb_service.search_articles(search_query) if search_query else self.kb_service.get_recent_articles()

        if not articles:
            st.info("No articles found")
            return

        for i, article in enumerate(articles):
            with st.expander(f"{article['title']} - {article['category']}"):
                st.markdown(article['content'])
                st.caption(f"Last updated: {article['last_updated']}")
                st.caption(f"Tags: {', '.join(article['tags'])}")
                
                # Add unique keys to any buttons
                if st.button(
                    "Save to Favorites",
                    key=f"favorite_article_button_{article['id']}"
                ):
                    # ... handle favoriting ...
                    pass

    def render_troubleshooting_section(self, search_query: str):
        """Render troubleshooting guides section"""
        st.subheader("Troubleshooting Guides")

        # Get troubleshooting guides
        guides = self.kb_service.search_guides(search_query) if search_query else self.kb_service.get_recent_guides()

        if not guides:
            st.info("No troubleshooting guides found")
            return

        for guide in guides:
            with st.expander(f"{guide['title']} - {guide['system']}"):
                st.markdown("### Problem Description")
                st.write(guide['problem'])
                
                st.markdown("### Solution Steps")
                for i, step in enumerate(guide['steps'], 1):
                    st.markdown(f"{i}. {step}")
                
                if guide.get('verification'):
                    st.markdown("### Verification")
                    st.write(guide['verification'])

    def render_stack_overflow_section(self, search_query: str):
        """Render Stack Overflow section"""
        st.subheader("Related Stack Overflow Posts")

        # Get Stack Overflow posts
        posts = self.kb_service.search_stack_overflow(search_query) if search_query else self.kb_service.get_top_posts()

        if not posts:
            st.info("No Stack Overflow posts found")
            return

        for post in posts:
            with st.expander(f"{post['title']} - Score: {post['score']}"):
                st.markdown(post['question'])
                st.markdown("### Accepted Answer")
                st.markdown(post['accepted_answer'])
                st.caption(f"Tags: {', '.join(post['tags'])}")

    def render_documentation_section(self, search_query: str):
        """Render documentation section"""
        st.subheader("Technical Documentation")

        # Get documentation
        docs = self.kb_service.search_documentation(search_query) if search_query else self.kb_service.get_recent_docs()

        if not docs:
            st.info("No documentation found")
            return

        for doc in docs:
            with st.expander(f"{doc['title']} - {doc['category']}"):
                st.markdown(doc['content'])
                st.caption(f"Last updated: {doc['last_updated']}") 