#!/usr/bin/env python3
"""
Vibelyo AI Content Generator
Uses Ollama (local LLM) to generate blog posts for Hugo

IMPORTANT: This script is DISABLED by default for safety.
To enable, set ENABLED=True in config.json

Safety Features:
- Requires manual activation
- Rate limiting
- Review workflow
- No auto-publishing (creates drafts)
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import requests

# Configuration file path
CONFIG_FILE = Path(__file__).parent / "config.json"
CONTENT_DIR = Path(__file__).parent.parent / "content"

class OllamaContentGenerator:
    """Generate blog content using Ollama API"""
    
    def __init__(self, config_path=CONFIG_FILE):
        """Initialize with configuration"""
        self.config = self.load_config(config_path)
        self.validate_config()
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {config_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file")
            sys.exit(1)
    
    def validate_config(self):
        """Validate configuration and check if enabled"""
        if not self.config.get('enabled', False):
            print("=" * 60)
            print("AI CONTENT GENERATION IS DISABLED")
            print("=" * 60)
            print("\nThis script is disabled by default for safety.")
            print("To enable, edit scripts/config.json and set 'enabled': true")
            print("\nIMPORTANT: Use responsibly and review all generated content")
            print("before publishing. Never auto-publish AI-generated content.")
            print("=" * 60)
            sys.exit(0)
        
        # Validate required fields
        required = ['ollama_api_url', 'model', 'categories']
        for field in required:
            if field not in self.config:
                print(f"Error: Missing required field '{field}' in config")
                sys.exit(1)
    
    def check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.config['ollama_api_url']}/api/tags")
            if response.status_code == 200:
                print("✓ Connected to Ollama successfully")
                return True
            else:
                print(f"✗ Ollama returned status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"✗ Cannot connect to Ollama at {self.config['ollama_api_url']}")
            print("  Make sure Ollama is running: ollama serve")
            return False
    
    def generate_content(self, prompt, max_tokens=2000):
        """Generate content using Ollama API"""
        url = f"{self.config['ollama_api_url']}/api/generate"
        
        payload = {
            "model": self.config['model'],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.get('temperature', 0.7),
                "top_p": self.config.get('top_p', 0.9),
                "num_predict": max_tokens
            }
        }
        
        try:
            print(f"Generating content with {self.config['model']}...")
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
        
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Try a shorter prompt.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: API request failed: {e}")
            return None
    
    def create_blog_post_prompt(self, topic, category, keywords):
        """Create a structured prompt for blog post generation"""
        prompt = f"""You are an expert content writer for an educational blog.

Write a comprehensive, beginner-friendly blog post about: {topic}

Category: {category}
Target Keywords: {keywords}

Requirements:
1. Write 1500-2000 words
2. Use clear, simple language for beginners
3. Include practical examples and actionable tips
4. Structure with H2 and H3 headings
5. Add a compelling introduction and conclusion
6. Focus on providing real value, not fluff
7. Be honest and realistic - no exaggerated claims
8. Include specific steps or strategies where applicable

Format the content in Markdown with:
- Clear heading hierarchy (## for H2, ### for H3)
- Bullet points and numbered lists where appropriate
- Short paragraphs (2-3 sentences)
- Bold text for emphasis where needed

Write ONLY the blog post content (no frontmatter, no title - just the content starting with introduction).
"""
        return prompt
    
    def create_frontmatter(self, title, description, category, tags, keywords):
        """Create Hugo frontmatter for the blog post"""
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:00")
        
        frontmatter = f"""---
title: "{title}"
description: "{description}"
date: {date}
draft: true
categories: ["{category}"]
tags: {json.dumps(tags)}
keywords: "{keywords}"
---

"""
        return frontmatter
    
    def sanitize_filename(self, title):
        """Convert title to valid filename"""
        # Remove special characters and convert to lowercase
        filename = title.lower()
        filename = ''.join(c if c.isalnum() or c.isspace() else '' for c in filename)
        filename = '-'.join(filename.split())
        filename = filename[:100]  # Limit length
        return f"{filename}.md"
    
    def save_post(self, category, filename, content):
        """Save generated post to content directory"""
        category_dir = CONTENT_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = category_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def generate_post(self, topic, category, title, description, tags, keywords):
        """Generate a complete blog post"""
        print(f"\n{'='*60}")
        print(f"Generating: {title}")
        print(f"Category: {category}")
        print(f"{'='*60}\n")
        
        # Create prompt
        prompt = self.create_blog_post_prompt(topic, category, keywords)
        
        # Generate content
        content_body = self.generate_content(prompt)
        
        if not content_body:
            print("✗ Content generation failed")
            return None
        
        # Create frontmatter
        frontmatter = self.create_frontmatter(title, description, category, tags, keywords)
        
        # Combine frontmatter and content
        full_content = frontmatter + content_body
        
        # Save to file
        filename = self.sanitize_filename(title)
        filepath = self.save_post(category, filename, full_content)
        
        print(f"\n✓ Post generated successfully!")
        print(f"  Location: {filepath}")
        print(f"  Status: DRAFT (review before publishing)")
        
        return filepath
    
    def interactive_mode(self):
        """Interactive mode for generating posts"""
        print("\n" + "="*60)
        print("VIBELYO AI CONTENT GENERATOR - INTERACTIVE MODE")
        print("="*60)
        
        # Select category
        print("\nAvailable categories:")
        categories = self.config['categories']
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        
        while True:
            try:
                choice = int(input("\nSelect category (number): "))
                if 1 <= choice <= len(categories):
                    category = categories[choice - 1]
                    break
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
        
        # Get post details
        print(f"\nCategory: {category}")
        topic = input("Enter topic/subject: ")
        title = input("Enter post title: ")
        description = input("Enter description (1-2 sentences): ")
        keywords = input("Enter keywords (comma-separated): ")
        tags_input = input("Enter tags (comma-separated): ")
        tags = [tag.strip() for tag in tags_input.split(',')]
        
        # Confirm
        print(f"\n{'='*60}")
        print("REVIEW YOUR INPUT:")
        print(f"{'='*60}")
        print(f"Category: {category}")
        print(f"Topic: {topic}")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Keywords: {keywords}")
        print(f"Tags: {tags}")
        print(f"{'='*60}")
        
        confirm = input("\nGenerate this post? (yes/no): ").lower()
        
        if confirm == 'yes':
            # Rate limiting
            if self.config.get('rate_limit_seconds', 0) > 0:
                print(f"\nRate limiting: waiting {self.config['rate_limit_seconds']} seconds...")
                time.sleep(self.config['rate_limit_seconds'])
            
            # Generate
            filepath = self.generate_post(topic, category, title, description, tags, keywords)
            
            if filepath:
                print(f"\n{'='*60}")
                print("NEXT STEPS:")
                print(f"{'='*60}")
                print(f"1. Review the generated content at: {filepath}")
                print(f"2. Edit and improve as needed")
                print(f"3. Change 'draft: true' to 'draft: false' when ready")
                print(f"4. Test locally: hugo server -D")
                print(f"5. Commit and push to publish")
                print(f"{'='*60}")
        else:
            print("\nCancelled.")

def main():
    """Main entry point"""
    generator = OllamaContentGenerator()
    
    # Check Ollama connection
    if not generator.check_ollama_connection():
        print("\nPlease start Ollama first:")
        print("  ollama serve")
        print("\nThen pull the model if you haven't:")
        print(f"  ollama pull {generator.config['model']}")
        sys.exit(1)
    
    # Run interactive mode
    generator.interactive_mode()

if __name__ == "__main__":
    main()
