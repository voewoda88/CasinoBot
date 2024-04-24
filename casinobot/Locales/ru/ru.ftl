start-text =
    <b>Добро пожаловать в наше виртуальное казино!</b>
    У вас на старте { $points } очков. Ваша ставка сейчас: { $bet }.

    <b>Внимание</b>: бот предназначен исключительно для демонстрации, и ваши данные могут быть сброшены в любой момент!
    Помните: лудомания — это болезнь, и никаких платных опций в боте нет.

    Убрать клавиатуру — /stop
    Показать клавиатуру, если пропала — /spin

start-game-text = ➡️Выбрать игру⬅️

choice-game-text = Выберите игру. <b>Но не забывайте</b>, это виртуальное казино, которое было создано <b>ИСКЛЮЧИТЕЛЬНО</b> в экспериментальных целях

spin-button-text = 🎰Слоты
black-jack-text = ♣️Black Jack
change-bet-text = 💲Изменить ставку

bet-text = Введите вашу ставку:
invalid-bet-text = Вы ввели неверную ставку. Повторите попытку.
complete-bet-text = Ваша ставка принята. Удачной игры!
bet-is-greater-than-balance-text = Ставка должна быть меньше, чем текущий баланс. Повторите попытку.

stop-text = Клавиатура удалена. Начать заново: /start, вернуть клавиатуру и продолжить: /spin

help-text =
    <b>У вас проблемы? Решайти их сами</b>. Мы слишком заняты.

    Исходный код бота доступен на <a href='https://github.com/voewoda88/CasinoBot'>GitHub</a>.

spin-fail = К сожалению, вы не выиграли.
spin-success =
    Вы выиграли {$score_change ->
         [one] {$score_change} очко
         [few] {$score_change} очка
        *[many] {$score_change} очков
    }!

after-spin =
    Ваша комбинация: { $combo_text } (№{ $dice_value }).
    { $result_text } Ваш счёт: <b>{ $new_score }</b>.


bet-is-greater-than-balance = Ставка должна быть меньше, чем текущий баланс.

zero-balance =
    Ваш баланс равен нулю. Вы можете смириться с судьбой и продолжить жить своей жизнью, а можете нажать /start, чтобы начать всё заново. Или /stop, чтобы просто убрать клавиатуру.

# Если не хотите использовать стикер, укажите это в конфиге
zero-balance-sticker = CAACAgIAAxkBAAEFGxpfqmqG-MltYIj4zjmFl1eCBfvhZwACuwIAAuPwEwwS3zJY4LIw9B4E

bar = BAR
grapes = виноград
lemon = лимон
seven = семь

menu-start = Перезапустить казино
menu-spin = Показать клавиатуру
menu-stop = Убрать клавиатуру
menu-help = Справочная информация
menu-games = Выбрать игру