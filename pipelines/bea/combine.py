with open('gdp_by_industry2.csv', 'r') as f1:
    original = f1.read()

with open('gdp_by_industry.csv', 'a') as f2:
    f2.write('\n')
    f2.write(original)