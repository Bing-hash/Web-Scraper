from ast import arg, arguments
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import threading







def check_if_link_visited(url):
    # Checks txt file to see if this url has already been scraped
    with open(f"links.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if (line == "URL: " + url+'\n'):
                return True
            
        return False

def check_if_link_in_text(url):
    # Checks txt file to see if this link is already listed, prevents duplicate links
    with open(f"links.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if (line == url+'\n'):
                return True
        return False





def get_all_website_urls(url, links):
    global total_links
    coun = 0
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    # this for loops should find all html and css files given the current url
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # empty href 
            continue
        # join the URL 
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove extra params
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        
        if href in links:
            # already in the set, prevents duplicate links
            continue
        if domain_name in href:
            
            # print(f"[*] Internal link: {href}") : used for testing
            
            if(check_if_link_in_text(href) == False):
                # check for duplicates, then add to list of links
                coun += 1
                links.add(href)
    
    # This should find all .js scripts
    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            script_url = urljoin(url, script.attrs.get("src"))
            links.add(script_url)
            
                
    # save the internal links to a file
    with open(f"links.txt", "a") as f:
        print(f"URL: " + url, file=f) 
        for link in links:
            print(link.strip(), file=f)    
    print(str(coun) + " links:")
    total_links += coun    
    


def scrape(url, count):
    global total_urls

    total_urls +=1
    print(f"------ Scraping: {url} ------")
    links = set()
    # Starts creating a thread for the scrape of the current url
    t = threading.Thread(target=get_all_website_urls, args=(url, links))
    t.start()
    t.join()

    # Checks if we are at the max depth given, if not, increment count and move on
    if (count >= depth):
            return
    count +=1
    # Looks at each link in links and scrape the links from them. Also check if this url has already been visited
    for link in links:
        
        if(check_if_link_visited(link) == False):
            scrape(link, count)
    
            



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Welcome to Python Web Scraper")
    parser.add_argument("domain",  help="The domain used to limit the links.")
    parser.add_argument("url", help="The starting URL.")
    parser.add_argument("depth", help="The depth at which to find links.", default=0)
    
    
    args = parser.parse_args()
    url = args.url
    depth = int(args.depth)
    domain_name = args.domain
    count = 0
    total_links = 0
    total_urls = 0
    with open(f"links.txt", "w") as f:
        print("Start", file=f) 

    threads = list()


    scrape(url, count)

    for n in range(5):
        print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    print('Scraped '+str(total_urls)+' total URLs:\n'+str(total_links)+' links found total:\nResults written to links.txt')


    
        