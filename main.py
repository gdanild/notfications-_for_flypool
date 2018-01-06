import telebot, threading,re,time,requests,ast

def get_stat(wallet):
    r = requests.get("https://api-zcash.flypool.org/miner/"+ wallet +"/currentStats").text
    r = ast.literal_eval(r)
    param = []
    if (r["status"]) == "OK":
        if r["data"]["validShares"] == 0:
            param.append("!!!doesn't work!!!")
            param.append("0")
            param.append("0")
        else:
            param.append("does work")
            param.append(r["data"]["usdPerMin"])
            param.append(r["data"]["averageHashrate"])
    return param
def st():
    while True:
        for i in wallets.keys():
            a = get_stat(i)
            for q in wallets[i]:
                const = 43200
                message = a[0] + "\nПрибыль(в мес.): " + str(int((float(a[1]) * const))) + "$\nСолей: " + str(int(float(a[2]))) +"Sol/s"
                bot.send_message(q, message)
        time.sleep(5)
def check_wallet(ls):
    for i in wallets.keys():
        search = re.findall(ls,i)
        if len(search)!=0:
            return False
    return True
def check_id(ls):
    ids = []
    for i in wallets.values():
        for q in i:
            ids.append(q)
    for i in ids:
        search = re.findall(ls,i)
        if len(search)!=0:
            return False
    return True

bot = telebot.TeleBot("503837165:AAG_lL-K87gmdtRP7MueIQs7mL_58WiRqy8")
threads = []
wallets = {}

t = threading.Thread(target=st)
threads.append(t)
t.start()

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if len(get_stat(message.text)) != 0:
        if check_id(message.chat.id) and check_wallet(message.text):
            wallets.update({message.text:[message.chat.id]})
            bot.send_message(message.chat.id, "Done, new wallets in base")
        elif check_id(message.chat.id) and check_wallet(message.text):
            get_value = wallets[message.text]
            get_value.append(message.chat.id)
            wallets.update({message.text:get_value})
            bot.send_message(message.chat.id, "Done, new user for this wallets")
        elif not check_id(message.chat.id) and not check_wallet(message.text):
            bot.send_message("Your wallets in base")
    else:
        bot.send_message(message.chat.id, "Bad wallet")
if __name__ == '__main__':
     bot.polling(none_stop=True)
