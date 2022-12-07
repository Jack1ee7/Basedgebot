import random
from Settings import pg_host, pg_user, pg_password, pg_title
from datetime import datetime, timezone
import psycopg2

connection = psycopg2.connect(
    host=pg_host,
    user=pg_user,
    password=pg_password,
    database=pg_title
)
connection.autocommit = True
cursor = connection.cursor()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS basedgebot(
    id serial,
    username text PRIMARY KEY,
    display_name text,
    is_admin boolean,
    is_muted boolean,
    reg_date timestamp,
    money real
    );'''
)

def pretty_console(message):
    return [message.author.display_name, f'({message.author.name})', 'Channel:', message.channel.name,
            datetime.now().strftime('%H:%M:%S'), ':', message.content]

def pg_add(username, display_name, count):
    cursor.execute(f"""INSERT INTO basedgebot 
    (id, username, display_name, is_admin, is_muted, reg_date, money)
    VALUES (DEFAULT, '{username}', '{display_name}', false, false, '{datetime.now(timezone.utc)}', 500.00);""")
    return f'-> New user {display_name} ({username}) was added to Database (+{count})'

def pg_mods():
    cursor.execute(f"""SELECT display_name
        FROM basedgebot WHERE is_admin = true;""")
    mods_list = []
    for x in cursor.fetchall():
        mods_list.append(x[0])

    mods_list = sorted(mods_list)
    return ', '.join(mods_list)

def is_mod(username):
    cursor.execute(f"""SELECT username
            FROM basedgebot WHERE is_admin = true;""")
    mods_list = []
    for x in cursor.fetchall():
        mods_list.append(x[0])

    if username in mods_list:
        return 1
    else:
        return

def is_muted(username):
    cursor.execute(f"""SELECT username
            FROM basedgebot WHERE is_muted = true;""")
    muted_list = []
    for x in cursor.fetchall():
        muted_list.append(x[0])

    if username in muted_list:
        return 1
    else:
        return 0

def is_real(username):
    cursor.execute(f"""SELECT display_name
                FROM basedgebot WHERE username = '{username}';""")
    real_list = cursor.fetchall()
    if len(real_list) != 0:
        return 1
    else:
        return 0

def mute_user(username):
    cursor.execute(f"""UPDATE basedgebot SET is_muted = true WHERE username = '{username}';""")

def unmute_user(username):
    cursor.execute(f"""UPDATE basedgebot SET is_muted = false WHERE username = '{username}';""")

def add_mod(username):
    cursor.execute(f"""UPDATE basedgebot SET is_admin = true WHERE username = '{username}';""")

def del_mod(username):
    cursor.execute(f"""UPDATE basedgebot SET is_admin = false WHERE username = '{username}';""")

def show_balance(username):
    cursor.execute(f"""SELECT money
            FROM basedgebot WHERE username = '{username}';""")
    money = cursor.fetchone()
    if money is None:
        cursor.execute(f"""SELECT money
                    FROM basedgebot WHERE display_name = '{username}';""")
        money = cursor.fetchone()

    return float('{:.2f}'.format(money[0]))

def show_displayname(username):
    cursor.execute(f"""SELECT display_name
                FROM basedgebot WHERE username = '{username}';""")
    display_name = cursor.fetchone()
    if display_name is None:
        cursor.execute(f"""SELECT display_name
                        FROM basedgebot WHERE display_name = '{username}';""")
        display_name = cursor.fetchone()
    return display_name[0]

def show_muted():
    flag = 'no one!'

    cursor.execute(f"""SELECT display_name
            FROM basedgebot WHERE is_muted = true;""")
    muted_list = []
    for x in cursor.fetchall():
        muted_list.append(x[0])

    muted_list = sorted(muted_list)

    if len(muted_list) != 0:
        flag = ', '.join(muted_list)

    return flag

def poop_decl(amount):
    amount = int(str(amount).split('.')[0]) % 10

    if amount == 1:
        return 'говняшка'
    elif 2 <= amount <= 4:
        return 'говняшки'
    else:
        return 'говняшек'

def amnesty_everyone():
    cursor.execute(f"""UPDATE basedgebot SET is_muted = false;""")

def dot_amount(amount):
    n = str(amount).split('.')
    number = ''
    k = 0
    for x in range(len(n[0])-1, -1, -1):
        k += 1
        number += n[0][x]
        if k % 3 == 0:
            number += ' '
    number = number[::-1] + '.' + n[1]

    return number

def get_slots_chance():
    cursor.execute(f"""SELECT money FROM basedgebot WHERE username = '%SLOTS_CHANCE%'""")
    return int(cursor.fetchone()[0])

def update_slots_chance(percent):
    cursor.execute(f"""UPDATE basedgebot SET money = {percent} WHERE username = '%SLOTS_CHANCE%'""")

def get_emotes(result):
    emotes_list = ['Kurica', 'Stronge', 'QuirkyYellowCat', 'kok', 'CallMe', 'HUH', 'Pobeda', 'WIDEGOSLINGREADY',
                   'wideCallMeHand', 'xddboss', 'Callme2', 'NASRAL', 'AlienUnpleased', 'OrangutanDrive', 'uzyVibe',
                   'uzyCatDance', 'Deadeg', 'EZeg', 'Turteg', 'Smoeg', 'OkayegUhavEg', 'OkayegBusiness', 'forsenLeave',
                   'egDespair', 'Gayeg', 'Frij', 'Zugreg', 'Amogeg', 'Okayeg', 'billyWink', 'LETSFUCKINGSRAAAT',
                   'oguzokDead', 'seregaJAM', 'Pridurki', '2HeadKostyan', 'Frens', 'ChefVAhue', 'ChefGorshok',
                   'Frenchge', 'uzyRolf', 'uzyRave', 'uzyJAM', 'UnDeadge', 'wheel100', 'happy', 'peepoVanish',
                   'DIESOFBEDGE', 'Opachki', 'uzyListening', 'roflanTanec', 'cowJAM', 'Shruge', 'vahui', 'Widevahui',
                   'Listening', 'happi', 'SHTO', 'ddx', 'VIBE', 'MMMM', 'NOOO', 'DIESOFGRINCH', 'RAGEY',
                   'TrollDespair', 'Aware', 'Clueless', 'WatchingStream', 'Basedge', 'uzyEgg', 'uzyNose', 'SratVechno',
                   'Srat', 'uzyStaring', '1984']

    match result:
        case 'win':
            random_num = random.randint(0, len(emotes_list)-1)
            return emotes_list[random_num], emotes_list[random_num], emotes_list[random_num]
        case 'loose':
            loose_1 = random.randint(0, len(emotes_list)-1)
            loose_2 = random.randint(0, len(emotes_list)-1)
            loose_3 = random.randint(0, len(emotes_list)-1)

            if random.randint(0, 1):
                match random.randint(0, 2):
                    case 0:
                        loose_1 = loose_2
                    case 1:
                        loose_2 = loose_3
                    case 2:
                        loose_1 = loose_3

            return emotes_list[loose_1], emotes_list[loose_2], emotes_list[loose_3]

def update_balance(username, amount):
    cursor.execute(f"""UPDATE basedgebot SET money = {amount} WHERE username = '{username}'""")

def slots_chance(win_chance):
    result = random.randint(1, 100)

    if 1 <= result <= win_chance:
        return 0
    elif 1 <= result <= 2:
        return 2
    else:
        return 1

def slots_game(win_chance, message, prefix, min_bet, max_bet, username):
    try:
        bet = float(message.split()[1])

        if len(message.split()) == 1:
            raise Exception
        elif bet < min_bet:
            return f'⚙️ {prefix}Минимальная ставка - {dot_amount(min_bet)} {poop_decl(min_bet)}'
        elif bet > max_bet:
            return f'⚙️ {prefix}Максимальная ставка - {dot_amount(max_bet)} {poop_decl(max_bet)}'

        emotes_win = get_emotes('win')
        emotes_loose = get_emotes('loose')

        random_cef = [2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
        jackpot_cef = 20

        match slots_chance(win_chance):
            case 0:
                win_amount = round(bet * random_cef[random.randint(0, len(random_cef)-1)], 2)
                update_balance(username, show_balance(username) + win_amount)
                return f'| {emotes_win[0]} | | {emotes_win[1]} | | {emotes_win[2]} | +{dot_amount(win_amount)} {poop_decl(win_amount)}. Баланс: {show_balance(username)} {poop_decl(show_balance(username))}'
            case 1:
                update_balance(username, show_balance(username) - bet)
                return f'| {emotes_loose[0]} | | {emotes_loose[1]} | | {emotes_loose[2]} | -{dot_amount(bet)} {poop_decl(bet)}. Баланс: {show_balance(username)} {poop_decl(show_balance(username))}'
            case 2:
                win_amount = round(bet * jackpot_cef, 2)
                update_balance(username, show_balance(username) + win_amount)
                return f'| {emotes_win[0]} | | {emotes_win[1]} | | {emotes_win[2]} | +{dot_amount(win_amount)} {poop_decl(win_amount)}. Баланс: {show_balance(username)} {poop_decl(show_balance(username))}'

    except Exception as e:
        print(e)
        return f'⚙️ {prefix}слоты <сумма ставки>'