# Screenshot

![Screenshot](https://github.com/KaVoshnik/control_pj/blob/master/screenshot.png?raw=true)

# How to use

Вы можете писать буковки в поле для ввода, имеются кнопки для создания, удаления, сохранения и настройки приложения заметок.

>> Настройки:
  - font - размер шрифта
  - theme - выбор темы(светлая/темная)

# Guide to install

Шаг 1:
Скачать репозеторий

Шаг 2:
Установить postgresql, настроить и запустить датабазу по следующим данным:

| Target              | content                                      |
| ------------------- | -------------------------------------------- |
| Database name       | notes_db                                     |
| user                | postgres                                     |
| Password            | 496284                                       |

>> Вы можеете использовать данный набор запросов для создания датабазы

    CREATE TABLE IF NOT EXISTS notes (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL
    )

Шаг 4:
Запустить exe
