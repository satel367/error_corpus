# Описание работы файлов
1. В файле load_data.py прогоняем код для парсинга ошибочных фраз и метаданных:
- Тексты должны быть размечены по этой схеме: \<phrase>[tag_1];[error_type_1]_[error_type_1_comment]/[tag_2];[error_type_2]{weight} и загружены в папку data/to_load.
- Цикл берет все тексты из папки data/to_load, прогоняет через регулярное выражение, добавляет ошибочные фразы и метаданные об ошибках в созданную ранее данных error_corpus.db. Тексты, прошедшие цикл, автоматически добавляются в папку data/loaded.
2. В файле plots.ipynb находятся различные фильтры, подсчет статистики и графики. Код можно использовать как основу,и менять детали под запрос. 
3. Файл delete_text.py содержит код для удаления текста конкретного студента из базы данных: удаляются все его данные и фразы. 
4. В файле main.py черновой код для тестирования корректной работы.
5. Файл groups.json нужен для верной работы функции SELECT в некоторых случаях, он содержит группировку тэгов по типам ошибок. Файл может дополняться. 

 # Схема базы данных 
 CREATE TABLE student
       (     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           name TEXT,
          level TEXT,
            simulation INTEGER,
           text TEXT
       );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE tag
       ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        tag TEXT
       );
CREATE TABLE type
       (       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       error_type TEXT,
           tag_id INTEGER,
        FOREIGN KEY(tag_id) REFERENCES tag(id)
       );
CREATE TABLE phrase
       (        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            phrase TEXT,
        student_id INTEGER,
           FOREIGN KEY(student_id) REFERENCES student(id)
       );
CREATE TABLE error
       (       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        phrase_id INTEGER,
           tag_id INTEGER,
          type_id INTEGER, comment TEXT, weight INTEGER,
          FOREIGN KEY(phrase_id) REFERENCES prase(id),
          FOREIGN KEY(tag_id) REFERENCES tag(id),
          FOREIGN KEY(type_id) REFERENCES type(id)
       );