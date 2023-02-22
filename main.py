from selenium import webdriver
from selenium.webdriver.common.by import By

selenium_driver_path = "DRIVER PATH" # THERE YOU HAVE ADD YOUR LOCALLY SELENIUM DRIVER PATH
driver = webdriver.Chrome(executable_path=selenium_driver_path)
driver.maximize_window()
driver.get("https://www.lotto.pl/zdrapki/katalog-zdrapek")

scratches = driver.find_elements(By.CLASS_NAME, "scratch-card-item__wrapper")
links = [scratch.get_attribute('href') for scratch in scratches]


def get_return_percentage(url):
    driver.get(url)

    quota = \
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div[3]/strong').get_attribute(
            'textContent').split("Nakład")[1].split("losów.")[0].replace(" ", "").replace("\xa0", "")

    ticket_cost = driver.find_element(By.XPATH,
                                      "/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div[4]/span["
                                      "2]/strong").get_attribute(
        'textContent').split()[0]

    columns = len(driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div['
                                                 '5]/table/tr[1]/td'))

    rows = len(driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div['
                                              '5]/table/tr'))

    win_prizes = []
    left_tickets = []

    for r in range(2, rows + 1):
        for c in range(1, columns + 1):
            value = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[2]/div["
                                                  "5]/table/tr[" + str(r) + "]/td[" + str(c) + "]")
            if c == 1:
                price = value.get_attribute('textContent')
                formatted_price = price.strip().replace("\xa0", "").replace("zł", "").strip()
                win_prizes.append(formatted_price)
            if c == 3:
                left_tickets.append(value.get_attribute('textContent'))

    int_win_prizes = [int(n) for n in win_prizes]
    int_left_tickets = [int(n) for n in left_tickets]

    cumulated_win_chance = []

    for n in range(len(int_left_tickets)):
        games_to_win = int(quota) / int_left_tickets[n]
        average_earn = int_win_prizes[n] / games_to_win
        cumulated_win_chance.append(round(average_earn, 4))

    percentage_of_return = round((sum(cumulated_win_chance) / int(ticket_cost)) * 100, 2)
    return int(percentage_of_return)


win_percentage_list = [get_return_percentage(link) for link in links]
win_dict = {k: v for (k, v) in zip(links, win_percentage_list)}
sorted_win_list = sorted(win_dict.items(), key=lambda x: x[1], reverse=True)

print(
    f"Najlepszą zdrapką jest {sorted_win_list[0][0]} z zwrotem {sorted_win_list[0][1]}%,\nDrugą najlepsza jest "
    f"{sorted_win_list[1][0]} z zwrotem {sorted_win_list[1][1]}%,\nTrzecią najlepsza zdrapką jest "
    f"{sorted_win_list[2][0]} z zwrotem {sorted_win_list[2][1]}%.")
