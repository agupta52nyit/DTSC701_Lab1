import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_faculty_urls(base_url):
    #HTTP GET request
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    #Find faculty URLs
    faculty_elements = soup.find_all('a', class_="underline hover:no-underline")
    faculty_urls = []
    for faculty_element in faculty_elements:
        faculty_url = urljoin(base_url, faculty_element['href'])
        faculty_urls.append(faculty_url)

    return faculty_urls

def scrape_faculty_info(faculty_url):
    #HTTP GET request
    response = requests.get(faculty_url)
    if response.status_code != 200:
        print(f"Failed: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    #Extract faculty names
    name_element = soup.select_one('#content > div > div.w-full.lg\\:w-2\\/3.px-4 > h1')
    faculty_name = name_element.get_text().strip() if name_element else "Name not available."

    #Extract faculty bio
    bio_element = soup.select_one('#content > div > div.w-full.lg\\:w-2\\/3.px-4 > div > p:nth-child(2)')
    faculty_bio = bio_element.get_text().strip() if bio_element else "Bio not available."

    #Extract courses taught
    courses_element = soup.select_one('#content > div > div.w-full.lg\\:w-2\\/3.px-4 > div > ul:nth-child(4)')
    faculty_courses = courses_element.get_text().strip() if courses_element else "Courses not available."

    return faculty_bio, faculty_courses, faculty_name

if __name__ == '__main__':
    base_url = 'https://engineering.wayne.edu/faculty'
    faculty_urls = scrape_faculty_urls(base_url)

    #Write URLs to bio_url.txt
    with open('bio_urls.txt', 'w') as file:
        for url in faculty_urls:
            file.write(url + '\n')
    print("Faculty URLs saved to bio_urls.txt.")

    #Scraping faculty info
    max_attempts = 3
    for url in faculty_urls:
        #Retry to handel 429 error
        attempts = 0
        while attempts < max_attempts:
            faculty_info = scrape_faculty_info(url)
            if faculty_info is not None:
                faculty_bio, faculty_courses, faculty_name = faculty_info

                #Write bio to bios.txt
                with open('bios.txt', 'a') as bio_file:
                    bio_file.write(faculty_name + ": " + faculty_bio + "\n")

                #Write cources taught to courses_taught.txt
                with open('courses_taught.txt', 'a') as courses_file:
                    courses_file.write(faculty_name + ": " + faculty_courses + "\n")
                break

            else:
                attempts += 1
                if attempts < max_attempts:
                    print(f"Error, Retry in 10s")
                    time.sleep(10) #Wait before retry
                else:
                    print(f"Error, Skipped")
                    break
    print("Bio saved to bios.txt")
    print("Courses taught saved to courses_taught.txt")
