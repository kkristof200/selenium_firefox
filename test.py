from selenium_firefox import Firefox

res = Firefox.generate_xpath('span', id_='custom_id', class_='custom-class', attributes={'key':'value'}, for_sub_element=True)
print(res)

f = Firefox('', '')
