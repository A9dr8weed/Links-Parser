import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

# number of urls visited so far will be stored here
total_urls_visited = 0

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)

    # This will make sure that a proper scheme (protocol, e.g http or https) and domain name exists in the URL.
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()

    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    # downloaded the HTML content of the web page and wrapped it with a soup object to ease HTML parsing.
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")

        if href == "" or href is None:
            # href empty tag
            continue

        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue

        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls = 30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl.
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)

    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls = max_urls)


if __name__ == "__main__":
    crawl("https://rozetka.com.ua/ua/notebooks/c80004/")

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse("https://rozetka.com.ua/ua/notebooks/c80004/").netloc

    # save the internal links to a file
    with open(f"C:\\Users\\Andrew\\Desktop\\{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # save the external links to a file
    with open(f"C:\\Users\\Andrew\\Desktop\\{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)