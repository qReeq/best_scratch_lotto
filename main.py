from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")
driver.maximize_window()
driver.get("https://www.lotto.pl/zdrapki/katalog-zdrapek")

# GET LINKS FOR ALL VISIBLE SCRATCHES ON SITE AND SAVING THEM ON A LIST
scratches = driver.find_elements(By.CLASS_NAME, "scratch-card-item__wrapper")
links = [scratch.get_attribute('href') for scratch in scratches]


def get_return_percentage(url):
    """ Input URL of the one scratch from lotto site.
    Taking and processing data like all and winning tickets, won prizes and cost of scratch.
    Returning % of statistically cost of return for one piece.
    """
    driver.get(url)

    # Getting number of all tickets for actual scratch
    quota = \
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div[3]/strong').get_attribute(
            'textContent').split("Nakład")[1].split("losów.")[0].replace(" ", "").replace("\xa0", "")

    # Getting cost of the actual scratch
    ticket_cost = driver.find_element(By.XPATH,
                                      "/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div[4]/span["
                                      "2]/strong").get_attribute(
        'textContent').split()[0]

    # Getting how much rows we have in table with win possibilities
    rows = len(driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div['
                                              '5]/table/tr'))

    win_prizes = []
    left_tickets = []

    # Getting values from column with prizes and tickets amount for these prizes.
    for c in range(2, rows + 1):
        driver_wins = driver.find_element(By.XPATH,
                                          "/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div["
                                          "5]/table/tr[" + str(c) + "]/td[1]")
        driver_tickets = driver.find_element(By.XPATH,
                                             "/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div["
                                             "5]/table/tr[" + str(c) + "]/td[3]")

        price = driver_wins.get_attribute('textContent')
        formatted_price = price.strip().replace("\xa0", "").replace("zł", "").strip()

        win_prizes.append(formatted_price)
        if driver_tickets.get_attribute('textContent') == "-":
            left_tickets.append(0)
        else:
            left_tickets.append(driver_tickets.get_attribute('textContent'))

    int_win_prizes = [int(n) for n in win_prizes]
    int_left_tickets = [int(n) for n in left_tickets]

    cumulated_win_chance = []

    # Calculating statistically return amount
    for n in range(len(int_left_tickets)):
        games_to_win = int(quota) / int_left_tickets[n]  # How much plays we need to win price from n row
        average_earn = int_win_prizes[n] / games_to_win  # Return value
        cumulated_win_chance.append(round(average_earn, 4))  # Cumulating all return values from all rows in table

    # Sum for all rows and getting of percentage return value
    percentage_of_return = round((sum(cumulated_win_chance) / int(ticket_cost)) * 100, 2)
    return int(percentage_of_return)


win_percentage_list = [get_return_percentage(link) for link in links]  # Making list of return percentages
win_dict = {k: v for (k, v) in zip(links, win_percentage_list)}  # Dict with link:return percentage
sorted_win_list = sorted(win_dict.items(), key=lambda x: x[1], reverse=True)  # Making sorted descending list for
# each key:value pair and closing them in the next list to easy access

print(
    f"Najlepszą zdrapką jest {sorted_win_list[0][0]} z zwrotem {sorted_win_list[0][1]}%,\nDrugą najlepsza jest "
    f"{sorted_win_list[1][0]} z zwrotem {sorted_win_list[1][1]}%,\nTrzecią najlepsza zdrapką jest "
    f"{sorted_win_list[2][0]} z zwrotem {sorted_win_list[2][1]}%.")
