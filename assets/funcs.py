import assets.config
from assets.parser import parser
from aiogram.methods import DeleteMessage


# get exchange rate 
rate_usdt_cny = parser.main()

#types:1:shoes 2:jackets 3:decoration 4: trousers, hoodie, sweter 5: t-shirt, shirt, shorts 



def get_price(cny, cl_type): 

    # formula = cny / rate + 0.02(cny / rate) + config.fee

    # return (cny / rate_usdt_cny) + 0.03 * (cny/rate_usdt_cny) + config.fee

    usdt = cny/rate_usdt_cny

    if (usdt > 300):
        if (cl_type == 1):
            return usdt + (usdt * 0.05) + 15
        if(cl_type == 2):
            return usdt + (usdt * 0.05) + 10
        if (cl_type == 3):
            return usdt + (usdt * 0.05)
        if (cl_type == 4):
            return usdt + (usdt * 0.05) + 5
        if (cl_type == 5):
            return usdt + (usdt * 0.05) + 2 
    else:
        if (cl_type == 1):
            return usdt + 30
        if(cl_type == 2):
            return usdt + 25
        if (cl_type == 3):
            return usdt + 15
        if (cl_type == 4):
            return usdt + 20
        if (cl_type == 5): 
            return usdt + 12



print(get_price(700, 1))
