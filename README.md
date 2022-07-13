# Data Has Power
Zadanie składało się z 2 części. Pierwsza część polegała na utworzeniu pliku docker-compose.yml, który będzie zarządzał serwisami Apache Spark (PySpark) i MySQL. Ponad to Spark powinien widzieć bazę MySQL oraz powinien mieć dostęp do lokalnego systemu plików w celu załadowania kodu/joba. Druga część zadania polegała na napisaniu skryptu w Pythonie (uruchamiany jako Sparkowy job), który pobierze plik (https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv) a następnie dokonuje na nim analizy odpowiadającej na pytania:
1. jaki procent dzieci (dziecko < 18 lat) przeżył katastrofę,
2. jaki procent dorosłych do 40 roku życia przeżył katastrofę,
3. jaki procent dorosłych do 40 roku życia przeżył katastrofę z podziałem na płeć,
4. jaki procent dorosłych powyżej 40 roku życia przeżył atastrofę,
5. jaki procent dorosłych powyżej 40 roku życia przeżył katastrofę z podziałem na płeć,
6. jaki procent przeżywalności był w danej klasie z podziałem na płeć.

Następnie wyniki miały zostać zapisane do bazy MySQL. Ponad to w repozytorium miał znaleźć się skrypt SQLowy, który utworzy tabele do zapisania wyników powyższej analizy.

W celu uruchomienia projektu wymagane jest również pobranie sterownika (https://dev.mysql.com/downloads/connector/j/) i zapisanie go w folderze quest.

## Wykorzystane komendy
Utworznie środowiska z plików dockera
```
docker-compose up
```
Dostanie się do konsoli sparka
```
sudo docker exec -it zadanie_spark_1 /bin/bash
```
Uruchomienie analizy
```
pyspark < code.py
```
Dostanie się do konsoli mysql
```
docker exec -it mysql mysql -u root -p 
```
Ususnięcie środowiska
```
docker-compose down --rmi all -v --remove-orphans
```
