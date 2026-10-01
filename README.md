# Real estate market analyser for rentals

This is project for educational purposes only. This is purely to see how to learn how to extract information from the known data.

## How it works

In this project I use multiple libraries such as ```matplotlib```, ``BeautifulSoup```, ```sqlite3```, and many more.

I took information out of the website and put it into a database where I order everything from:
- price
- rent
- liveable space
- neighbourhood
- link of the listing
- name

There were unusual amount of listings with very odd price ranges, so I decided through an if statement to only pick listings within a reasonable range, and the rest to add it into a separate table.

