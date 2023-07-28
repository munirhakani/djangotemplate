def getPrice(cost):
    if .01 <= cost <= .75:
        price = round((cost + .25)*4)/4
    elif .76 <= cost <= 1.50:
        price = round((cost + .50)*4)/4
    elif 1.51 <= cost <= 2.25:
        price = round((cost + 0.75)*4)/4
    elif 2.26 <= cost <= 3.5:
        price = round((cost + 1)*4)/4
    elif 3.51 <= cost <= 5:
        price = round((cost + 1.25)*4)/4
    elif 5.01 <= cost <= 6:
        price = round((cost + 1.5)*4)/4
    elif 6.01 <= cost <= 7:
        price = round((cost + 1.75)*4)/4
    elif 7.01 <= cost <= 8:
        price = round((cost + 2)*4)/4
    elif 8.01 <= cost <= 9:
        price = round((cost + 1.8)*4)/4
    elif 9.01 <= cost <= 10:
        price = round((cost + 2)*4)/4
    elif 10.01 <= cost <= 15:
        price = round((cost + 3)*4)/4
    elif 15.01 <= cost <= 20:
        price = round((cost + 4)*4)/4
    elif 20.01 <= cost <= 25:
        price = round((cost + 5)*4)/4
    elif 25.01 <= cost <= 30:
        price = round((cost + 6)*4)/4
    elif 30.01 <= cost <= 35:
        price = round((cost + 7)*4)/4
    elif 35.01 <= cost <= 40:
        price = round((cost + 8)*4)/4
    elif 40.01 <= cost <= 45:
        price = round((cost + 9)*4)/4
    elif 45.01 <= cost <= 50:
        price = round((cost + 10)*4)/4
    elif 50.01 <= cost <= 55:
        price = round((cost + 10)*4)/4
    elif 55.01 <= cost <= 60:
        price = round((cost + 10)*4)/4
    elif 60.01 <= cost <= 65:
        price = round((cost + 10)*4)/4
    elif 65.01 <= cost <= 70:
        price = round((cost + 10.75)*4)/4
    elif 70.01 <= cost <= 75:
        price = round((cost + 11.5)*4)/4
    elif 75.01 <= cost <= 80:
        price = round((cost + 12.25)*4)/4
    elif 80.01 <= cost <= 85:
        price = round((cost + 13)*4)/4
    elif 85.01 <= cost <= 90:
        price = round((cost + 13.5)*4)/4
    elif 90.01 <= cost <= 95:
        price = round((cost + 14)*4)/4
    elif 95.01 <= cost <= 100:
        price = round((cost + 15)*4)/4
    else:
        price = round((cost + 15)*4)/4
    return price