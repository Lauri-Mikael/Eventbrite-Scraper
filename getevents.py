import requests
from bs4 import BeautifulSoup
from image_down import image_down
from datetime import date

def get_events(area):

    page_num = 1

    # Create an empty list to store the event data
    event_data = []

    number = 1

    while True:
        # URL to SOUP
        url = f'https://www.eventbrite.com/d/united-states--{area}/events--this-week/?page={page_num}'
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        print("Still Running")

        # Find all the event listings on the page
        event_listings = soup.find_all('div', class_='Container_root__16e3w NestedActionContainer_root__1jtfr event-card event-card__horizontal horizontal-event-card__action-visibility')

        # To out or not
        if len(event_listings) <= 2:
            break
        page_num += 1

        # Loop through each event listing and extract the event data
        
        for event in event_listings:

            # Extract the event title and link
            title = event.find('h2', class_='Typography_root__4bejd #3a3247 Typography_body-lg__4bejd event-card__clamp-line--two Typography_align-match-parent__4bejd').text.strip()
            link = event.find('a')['href']

            # Extract date and place
            dateplace = event.find_all('p', class_='Typography_root__4bejd #585163 Typography_body-md__4bejd event-card__clamp-line--one Typography_align-match-parent__4bejd')

            if not len(dateplace) == 2:
                continue

            # Extract the event date
            dates = dateplace[0]

            # Extract the event place
            place = dateplace[1]

            # Extract image
            image = event.find('img', class_='event-card-image')

            if image == None:
                continue
    
            dates = dates.text.strip()

            # Add Thursday Exception

            day_of_week = date.today().weekday()

            if not (dates[:3] == "Fri" or (day_of_week == 3 and dates[:3] == "Tom")):
                continue

            splitdate = dates.split(" • ")
            day = splitdate[0]
            if day[:3] == "Tom":
                day = "Friday"
            eventtime = splitdate[1]

            if "+" in eventtime:
                times = eventtime.split(" + ")
                additional = times[1][:1]
                eventtime = times[0]
            else:
                additional = ""

            place = place.text.strip()
            image_url = image['src']
            image_name = image_down(image_url, number, area)
            number += 1
            event_data.append([title, link, day, eventtime, additional, place, image_name])

    page_num = 1
    while True:
        # URL to SOUP
        url = f'https://www.eventbrite.com/d/united-states--{area}/events--this-weekend/?page={page_num}'
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the event listings on the page
        event_listings = soup.find_all('div', class_='Container_root__16e3w NestedActionContainer_root__1jtfr event-card event-card__horizontal horizontal-event-card__action-visibility')

        # To out or not
        if len(event_listings) <= 2:
            break
        page_num += 1

        # Loop through each event listing and extract the event data
        
        for event in event_listings:

            # Extract the event title and link
            title = event.find('h2', class_='Typography_root__4bejd #3a3247 Typography_body-lg__4bejd event-card__clamp-line--two Typography_align-match-parent__4bejd').text.strip()
            link = event.find('a')['href']

            # Extract date and place
            dateplace = event.find_all('p', class_='Typography_root__4bejd #585163 Typography_body-md__4bejd event-card__clamp-line--one Typography_align-match-parent__4bejd')

            if not len(dateplace) == 2:
                continue

            # Extract the event date
            dates = dateplace[0]

            # Extract the event place
            place = dateplace[1]

            # Extract image
            image = event.find('img', class_='event-card-image')

            if image == None:
                continue
    
            dates = dates.text.strip()

            if not (dates[:3] == "Sat" or dates[:3] == "Sun"):
                continue
                    
            splitdate = dates.split(" • ")
            day = splitdate[0]
            eventtime = splitdate[1]

            if "+" in eventtime:
                times = eventtime.split(" + ")
                additional = times[1][:1]
                eventtime = times[0]
            else:
                additional = ""

            place = place.text.strip()
            image_url = image['src']
            image_name = image_down(image_url, number, area)
            number += 1
            event_data.append([title, link, day, eventtime, additional, place, image_name])

    return event_data
