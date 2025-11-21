from bs4 import BeautifulSoup
import re
import base64

def parse_quiz_page(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # 1. Extract visible text
    text = soup.get_text(separator="\n", strip=True)

    # 2. Extract all links
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # 3. Find JavaScript base64 content (many quiz pages use atob())
    base64_blocks = []
    scripts = soup.find_all("script")

    for script in scripts:
        if script.string:
            matches = re.findall(r'atob\(`([^`]+)`\)', script.string)
            for block in matches:
                try:
                    decoded = base64.b64decode(block).decode("utf-8")
                    base64_blocks.append(decoded)
                except:
                    pass

        # Try discovering submit URL in links
    submit_url = None
    for link in links:
        if "submit" in link.lower():
            submit_url = link
            break

    return {
        "text": text,
        "links": links,
        "base64_data": base64_blocks,
        "submit_url": submit_url
    }


    # Detect submit URL from visible text (usually provided)
    submit_url = None
    for link in links:
        if "submit" in link.lower():
            submit_url = link

    return {
        "text": text,
        "links": links,
        "base64_data": base64_blocks,
        "submit_url": submit_url
    }


