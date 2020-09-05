import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)

    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('li')
    pages = []
    for link in links[1:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")

    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()

    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    link = html.find("h2", {"class": "title"}).find("a")["href"]
    if "http" in link:
        href = f"{link}"
    else:
        href = f"https://www.indeed.com{link}"

    return {
        'title': title,
        'company': company,
        'location': location,
        'link': href
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Loading indeed page {page}")
        result = requests.get(f"{url}&start={page*10}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://www.indeed.com/jobs?q={word}&l=Irvine%2C%20CA&limit=10"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
