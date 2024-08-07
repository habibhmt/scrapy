import scrapy
import re

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["anthropic.com"]
    start_urls = ["https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering"]

    def parse(self, response):
        title = response.css('h1::text').get().strip()
        sections = []

        for section in response.css('main > h2, main > p, main > ul'):
            if section.css('h2'):
                sections.append({
                    "section": section.css('::text').get().strip(),
                    "content": ""
                })
            elif sections:
                if section.css('p'):
                    content = ' '.join(section.css('::text').getall()).strip()
                    sections[-1]["content"] += content + "\n\n"
                elif section.css('ul'):
                    for li in section.css('li'):
                        content = ' '.join(li.css('::text').getall()).strip()
                        sections[-1]["content"] += f"- {content}\n"
                    sections[-1]["content"] += "\n"

        # Clean up content
        for section in sections:
            section['content'] = re.sub(r'\s+', ' ', section['content']).strip()
            section['content'] = section['content'].replace(' .', '.')
            section['content'] = section['content'].replace(' ,', ',')

        yield {
            "title": title,
            "content": sections
        }