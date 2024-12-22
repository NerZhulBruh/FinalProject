# FinalProject

Проект по анализу датасета, содержащего рейтинг фильмов по мнения iMBD [IMDb Dataset Top-Rated films 1898-2022](https://www.kaggle.com/datasets/digvijaysinhgohil/imdb-dataset-toprated-films-18982022/code).

## Требования
- Python 3.7+
- Chrome Browser 115+ версии, и вот с этой странички https://developer.chrome.com/docs/chromedriver/downloads?hl=ru  скачать Google Chrome for Testing для вашей версии Chrome и вашей ОС.
- Установленные библиотеки: selenium, os, pandas, time, dash, plotly, matplotlib.pyplot, seaborn, re 
- Установленные VisualStudioCode либо PyCharm

## Установка и запуск
1. Скачайте файл main.py и датасет с [IMDb Dataset Top-Rated films 1898-2022](https://www.kaggle.com/datasets/digvijaysinhgohil/imdb-dataset-toprated-films-18982022/code);
2. Откройте их в одной из сред;
3. Запустите файл и подождите выполнения;
4. Пройдите по предоставленной после выполнения ссылке либо введите в строку ссылки браузера:http://127.0.0.1:8050;
5. Готово, вы наблюдаете дашборд.

## Ход работы
1. Определился с тематикой исследования и нашел подходящий датасет;
2. Так же нашел сайт способный обогатить мои данные;
3. Собрал данные с сайта с помощью Selenium и преобразил их в датафрейм;
4. Обработал получившиеся датафреймы для корректного преобразования в графики;
5. Составил дашборд;
6. Приступил к оценочному анализу получившегося дашборда;
7. Подвел итоги оценочного анализа, написав выводы по рвботе.

## Выводы
### Оба датасета демонстрируют, что:
 - жанры драма,экшн,приключения являются лидерами по количеству выпущенных фильмов за всю историю кинематографа, причем драма более чем в 2 раза отрывается от ближайшего конкурента(экшн/боевики);
 - в ходе исследования не было выявлено зависимостей между годом выпуска кино и его оценкой, а так же между оценкой и длительностью фильма, но прослеживается незначительная зависимость года выпуска и длительности,но столь малая, что не может быть полезна на практике;
 - золотой серединой длительности фильма для зрителя является интервал от 140 до 200 минут, так как именно в нем прослеживается наибольшее число высоких оценок;
 - после отметки ~210-220 минут оценки фильмов резко идут вниз, пробивая медиану, быть может из-за того что на протяжении столь длительного времени человеку становится уже тяжело удерживать внимания и с точность понимать повествование и мотивы картины;
 - зачастую наибольшего рейтинга удостаиваются фильмы с прокатным рейтингом 15+, что может в целом логично: они доступны для большей части аудитории, больший творческий простор для создателей, больше шанс на успешное донесение авторской мысли с не самыми банальными посылами;
 - динамика выхода фильмов по годам в двух рахных источников в целом показывает одинаковые тенденции, если рассматривать периодами: первый большой "бум" в семидесятых, второй в девяностых, в нулевых же присутсвуют различия, но в обоих источниках наиболее явно виден спад выпуска в 2019 года обусловленный пандемией короновируса.
   
