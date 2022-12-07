from twitchio.ext.commands import Context
from Settings import main_token, channels, prefix
from Bot import pg_add, pg_mods, is_mod, is_muted, mute_user, is_real, unmute_user, add_mod, del_mod, \
    show_balance, show_displayname, show_muted, poop_decl, amnesty_everyone,\
    dot_amount, slots_game, get_slots_chance, update_slots_chance
from datetime import datetime
from twitchio import Channel
from twitchio.ext import commands

# TODO:
#       добавить протекцию от бана в БД

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=main_token,
            prefix=prefix,
            initial_channels=channels,
            case_insensitive=True)
        self.time_start = datetime.now()
        self.delay = None
        self.count = 0
        self.tumbler = True
        self.min_bet = 10.0
        self.max_bet = 1000000000000.0

    async def event_channel_joined(self, channel: Channel):
        self.delay = datetime.now() - self.time_start
        print('Launched in ', f'{self.delay.seconds}.{self.delay.microseconds//10000}', 's', sep='')
        print('Basedgebot v1.0')

    async def event_ready(self):
        print(f'Logged in as | {self.nick.capitalize()}')
        print(f'User id is | {self.user_id}')

    async def event_command_error(self, context: Context, error: Exception) -> None:
        # raise error
        pass

    async def event_message(self, message):
        if message.echo:
            return

        if not(is_real(message.author.name)):
            self.count += 1
            print(pg_add(message.author.name, message.author.display_name, self.count))

        message.content = ' ' + message.content
        if not(is_muted(message.author.name)):
            await self.handle_commands(message)

    async def global_before_invoke(self, ctx: commands.Context):
        print(f'-> Command "{ctx.message.content.split()[0]}" was called')

    # Control panel
    @commands.command(name='admin')
    async def admin_menu(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            await ctx.reply(f'⚙️ Панель управления. '
                            f'{prefix}list, {prefix}mute, {prefix}unmute, {prefix}op, '
                            f'{prefix}delop, {prefix}showmuted, {prefix}on, {prefix}off, '
                            f'{prefix}unbanall, {prefix}slotschance')

    @commands.command(name='list')
    async def list_menu(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            await ctx.reply(f'⚙️ Список модераторов: {pg_mods()}')

    @commands.command(name='mute')
    async def mute_menu(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            message = ctx.message.content.split()
            try:
                username = message[1].strip('@').lower()

                if is_muted(username):
                    await ctx.reply(f'⚙️ {show_displayname(username)} уже заглушен, используй {prefix}unmute')
                elif not(is_muted(username)):
                    if is_real(username):
                        if not(is_mod(username)):
                            mute_user(username)
                            await ctx.reply(f'⚙️ {show_displayname(username)} заглушен!')
                        else:
                            await ctx.reply(f"⚙️ Ты не можешь заглушить модератора!")
                    else:
                        await ctx.reply(f'⚙️ Игрока {username.capitalize()} не существует')
            except:
                await ctx.reply(f'⚙️ {prefix}mute <никнейм>')

    @commands.command(name='unmute')
    async def unmute_menu(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            message = ctx.message.content.split()
            try:
                username = message[1].strip('@').lower()
                if is_muted(username):
                    unmute_user(username)
                    await ctx.reply(f'⚙️ {show_displayname(username)} больше не заглушен!')
                elif not(is_muted(username)):
                    if is_real(username):
                        await ctx.reply(f'⚙️ {show_displayname(username)} не был заглушен!')
                    else:
                        await ctx.reply(f'⚙️ Игрока {username.capitalize()} не существует')
            except:
                await ctx.reply(f'⚙️ {prefix}unmute <никнейм>')

    @commands.command(name='op')
    async def give_op(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            message = ctx.message.content.split()
            try:
                username = message[1].strip('@').lower()
                if is_mod(username):
                    await ctx.reply(f'⚙️ {show_displayname(username)} уже модератор!')
                elif not(is_mod(username)):
                    if is_real(username):
                        add_mod(username)
                        await ctx.reply(f'⚙️ {show_displayname(username)} теперь модератор!')
                    else:
                        await ctx.reply(f'⚙️ Игрока {username.capitalize()} не существует')
            except:
                await ctx.reply(f'⚙️ {prefix}op <никнейм>')

    @commands.command(name='delop')
    async def part_op(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            message = ctx.message.content.split()
            try:
                username = message[1].strip('@').lower()
                if is_mod(username):
                    if username == 'basedgebot':
                        await ctx.reply('может ты нахуй пойдешь?')
                    else:
                        del_mod(username)
                        await ctx.reply(f'⚙️ {show_displayname(username)} больше не модератор!')
                elif not(is_mod(username)):
                    if is_real(username):
                        await ctx.reply(f'⚙️ {show_displayname(username)} не был модератором!')
                    else:
                        await ctx.reply(f'⚙️ Игрока {username.capitalize()} не существует')
            except:
                await ctx.reply(f'⚙️ {prefix}delop <никнейм>')

    @commands.command(name='showmuted')
    async def mutelist_menu(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            mute_output = show_muted()
            if 40 + len(mute_output) > 430:
                mute_output = mute_output[:430] + '...'
            await ctx.reply(f'⚙️ Список заглушенных пользователей: {mute_output}')

    @commands.command(name='off')
    async def off_tumbler(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            self.tumbler = False
            await ctx.reply(f'⚙️ Бот выключен!')

    @commands.command(name='on')
    async def on_tumbler(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            self.tumbler = True
            await ctx.reply(f'⚙️ Бот включен!')

    @commands.command(name='unbanall')
    async def unban_all(self, ctx: commands.Context):
        if is_mod(ctx.author.name):
            amnesty_everyone()
            await ctx.reply(f'⚙️ Объявлена амнистия!')

    @commands.command(name='slotschance')
    async def slots_chance(self, ctx: commands.Context):
        if self.tumbler or is_mod(ctx.author.name):
            try:
                percent = int(ctx.message.content.split()[1])
                if percent > 99:
                    percent = 99
                elif percent < 1:
                    percent = 1
                update_slots_chance(percent)
                await ctx.reply(f'⚙️ Шанс выигрыша в слотах теперь - {percent}%')
            except:
                await ctx.reply(f'⚙️ Шанс выигрыша в слотах - {get_slots_chance()}%')

    # User panel
    @commands.cooldown(1, 15, commands.Bucket.member)
    @commands.command(name='баланс')
    async def balance_menu(self, ctx: commands.Context):
        if self.tumbler or is_mod(ctx.author.name):
            message = ctx.message.content.split()
            if len(message) == 1:
                username = ctx.author.name
                await ctx.reply(f'💶 Баланс {ctx.author.display_name}: {dot_amount(show_balance(username))} {poop_decl(show_balance(username))}')
            elif len(message) > 1:
                username = message[1].strip('@')
                try:
                    await ctx.reply(f'💶 Баланс {show_displayname(username)}: {dot_amount(show_balance(username))} {poop_decl(show_balance(username))}')
                except:
                    await ctx.reply(f'💶 Игрока {message[1]} не существует')

    # Game panel
    @commands.cooldown(1, 3, commands.Bucket.member)
    @commands.command(name='слоты')
    async def slots_menu(self, ctx: commands.Context):
        if self.tumbler or is_mod(ctx.author.name):
            await ctx.reply(f'{slots_game(get_slots_chance(), ctx.message.content, prefix, self.min_bet, self.max_bet, ctx.author.name)}')

if __name__ == '__main__':
    bot = Bot()
    bot.run()