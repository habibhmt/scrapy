import pytest
from scrapy.http import HtmlResponse
from scrapy.http import Request
from myproject.spiders.example import ExampleSpider

@pytest.fixture
def response():
    url = "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview"
    request = Request(url=url)
    html_content = """
    <html>
    <body>
        <main>
            <h1>Prompt Engineering Overview</h1>
            <h2>Introduction</h2>
            <p>This is an introduction to prompt engineering.</p>
            <h2>Details</h2>
            <ul>
                <li>Detail 1</li>
                <li>Detail 2</li>
            </ul>
        </main>
    </body>
    </html>
    """
    return HtmlResponse(url=url, request=request, body=html_content, encoding='utf-8')

def test_parse(response):
    spider = ExampleSpider()
    result = next(spider.parse(response))
    
    assert result['title'] == "Prompt Engineering Overview"
    assert len(result['content']) == 2
    assert result['content'][0]['section'] == "Introduction"
    assert result['content'][0]['content'] == "This is an introduction to prompt engineering."
    assert result['content'][1]['section'] == "Details"
    assert result['content'][1]['content'] == "- Detail 1 - Detail 2"