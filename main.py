import datetime
import sqlite3

import now as now
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
now = datetime.datetime.now()

#создание бд
con = sqlite3.connect("bicycle.sqlite")
cursor = con.cursor()
con.executescript('''

DROP TABLE IF EXISTS TypeBicycle;

CREATE TABLE IF NOT EXISTS TypeBicycle(
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name VARCHAR(45),
    price_type INTEGER
);

DROP TABLE IF EXISTS ModelBicycle;

CREATE TABLE IF NOT EXISTS ModelBicycle(
    id_model INTEGER PRIMARY KEY AUTOINCREMENT,
    name_model VARCHAR(45),
    release_year INTEGER,
    id_brand INTEGER NOT NULL
    CONSTRAINT fk_ModelBicycle_BrandBicycle1,   
        FOREIGN KEY (id_brand) REFERENCES BrandBicycle (id_brand)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS BrandBicycle;

CREATE TABLE IF NOT EXISTS BrandBicycle(
    id_brand INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name VARCHAR(45),
    id_type INT
    CONSTRAINT fk_BrandBicycle_TypeBicycle1,   
        FOREIGN KEY (id_type) REFERENCES TypeBicycle (id_type)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS bike;

CREATE TABLE IF NOT EXISTS bike(
    id_bike INTEGER PRIMARY KEY AUTOINCREMENT,
    year_issue DATE,
    id_model INTEGER
    CONSTRAINT fk_bike_BrandModelBicycle1,
        FOREIGN KEY (id_model) REFERENCES BrandBicycle (id_model)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS client;

CREATE TABLE IF NOT EXISTS client(
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(80),
    phone_num INTEGER,
    date_birth DATE,
    date_regist DATE
);

DROP TABLE IF EXISTS bike_rental;

CREATE TABLE IF NOT EXISTS bike_rental(
    idbike_rental INTEGER PRIMARY KEY AUTOINCREMENT,
    date_issue DATE,
    date_return DATE,
    price INTEGER NULL,
    id_bike INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    CONSTRAINT fk_bike_rental_bike1,
        FOREIGN KEY (id_bike) REFERENCES bike (id_bike)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_bike_rental_client1,
        FOREIGN KEY (id_client) REFERENCES client (id_client)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS damage_type;

CREATE TABLE IF NOT EXISTS damage_type(
    id_damage INTEGER PRIMARY KEY AUTOINCREMENT,
    damage_name VARCHAR(45),
    damage_price INTEGER  
);

DROP TABLE IF EXISTS rental_journal;

CREATE TABLE IF NOT EXISTS rental_journal(
    id_journal INTEGER PRIMARY KEY AUTOINCREMENT,
    damage_sum INTEGER,
    description MEDIUMTEXT,
    id_damage INTEGER,
    idbike_rental INTEGER,
    CONSTRAINT fk_rental_journal_bike_rental1,
    FOREIGN KEY (idbike_rental) REFERENCES bike_rental (idbike_rental)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_rental_journal_damage_type1,
    FOREIGN KEY (id_damage) REFERENCES damage_type (id_damage)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);
''')
con.commit()

con.executescript('''
INSERT INTO client (full_name, phone_num, date_birth, date_regist)  VALUES 
('Вилков Арсений Евгеньевич',89503457612,'1980-09-17','2019-10-01'),
('Дровяная Ангелина Валерьевна',89630000111,'1992-02-23','2020-06-11'),
('Коровко Ева Федоровна',89516667374,'1997-11-07','2019-09-03'),
('Понасенков Евгений Николаевич',89588764310,'2003-07-15','2020-11-21'),
('Зарубин Дмитрий Петрович',89503471992,'2004-10-17','2021-03-22'),
('Даркариева Мария Александровна',89993357002,'1999-10-18','2021-05-13'),
('Волосатина Кристина Сергеевна',89123458880,'1989-05-26','2020-07-19'),
('Прушкин Прокопий Прокопьевич',89512455452,'1998-04-09','2019-02-29'),
('Гипосфиленко Геннадий Иванович',89763458612,'2001-12-05','2020-06-06'),
('Гербер Татьяна Викторовна',89506187632,'1999-02-11','2019-05-27'),
('Краснюк Сергей валерьевич',89511157644,'2002-08-30','2020-04-24');

INSERT INTO ModelBicycle (name_model, release_year,id_brand) VALUES
('Weekend', 2018,1),
('Edge', 2019,1),
('Navigator 210 Gent 26', 2016,3),
('Barcelona Air 2.0',2018,6),
('Legend',2018,2),
('Adrenalin MD 27.5" V010',2019,4),
('TIMBA 20',2022,7),
('C243DW 24',2022,9),
('IMPULSE 28 X D',2022,8),
('XT 300 V010',2020,8),
('Stance E+ 1 29er 25km/h',2021,10),
('GFR F/W',2018,11),
('Tyrant 20',2016,5);

INSERT INTO TypeBicycle (type_name, price_type) VALUES
('Городской',1500),
('Горный',2500),
('Детский',1000),
('Гоночный',3500),
('Электро',2000),
('BMX',2500);

INSERT INTO BrandBicycle (brand_name,id_type) VALUES
('ASPECT',1),
('ASPECT',2),
('STELS',1),
('STELS',2),
('STELS',6),
('FORWARD',1),
('FORWARD',3),
('FORWARD',4),
('AVENGER',3),
('GIANT',5),
('GIANT',6);

INSERT INTO bike (year_issue,id_model) VALUES
(2021,1),
(2021,1),
(2021,1),
(2021,2),
(2021,2),
(2017,3),
(2017,3),
(2017,3),
(2017,3),
(2019,4),
(2019,5),
(2021,6),
(2021,6),
(2022,7),
(2022,7),
(2022,7),
(2022,8),
(2022,9),
(2021,10),
(2021,10),
(2021,10),
(2022,11),
(2022,11),
(2022,11),
(2019,12),
(2019,12),
(2018,13),
(2018,13),
(2018,13);

INSERT INTO damage_type ( damage_name, damage_price) VALUES
('Утеря велосипеда',25000),
('Рама, замок блокировки',10000),
('Передняя вилка, руль, колесо, диск колеса, тормоза колесные',5000),
('Цепь, корзина, седло, батарея, покрышка',3000),
('Звонок, фонарик, педаль, тормозная ручка, грипсы',1000),
('Утеря электровелосипеда',35000),
('Аккумулятор, доп.аккумулятор',10000),
('Приборная панель, механизм складывания',5500),
('Трекер',10000);

INSERT INTO rental_journal (damage_sum,description,id_damage,idbike_rental) VALUES
(4000,'Пробита покрышка',3,3),
(5000,'Вмятина на раме',2,21),
(11500,'Аккумулятор залит водой',7,16),
(1000,'Разбит фонарик',5,4),
(1500,'Утеряна педаль',5,8),
(5500,'Испорчен механизм складывания',8,5),
(10000,'Утерян трекер',9,15),
(3500,'Повреждение корзины',4,18),
(5000,'Повреждение колесных тормозов',3,11),
(3000,'Повреждения покрытия седла',4,12);

INSERT INTO bike_rental (date_issue, date_return, id_client, id_bike) VALUES
('2020-06-12','2020-06-15',2,10),
('2019-10-12','2019-10-13',10,7),
('2022-08-03','2022-08-10',6,17),
('2021-10-20','2021-10-22',1,5),
('2021-09-17','2021-09-21',9,13),
('2021-05-28','2021-06-03',11,25),
('2022-04-19','2022-04-23',6,15),
('2022-05-23','2022-05-24',5,22),
('2021-07-05','2021-07-08',3,17),
('2021-06-01','2021-07-01',11,22),
('2021-04-06','2021-04-08',9,11),
('2021-08-03','2021-08-13',5,11),
('2021-09-16','2021-09-17',5,19),
('2022-06-14','2022-06-15',10,22),
('2022-06-21','2022-06-23',4,18),
('2021-07-20','2021-07-27',11,12),
('2019-07-21','2019-07-24',8,27),
('2020-10-18','2020-10-19',7,9),
('2020-10-05','2020-10-23',5,6),
('2021-09-02','2021-09-07',6,19),
('2020-04-29','2020-05-11',1,11),
('2019-04-28','2019-06-14',8,27),
('2022-05-15','2022-05-21',4,18);
''')

con.commit()

print('1--------------------')

#Запрос на выборку информации о велосипеде, с указанием года поступления и типа велосипеда.
#Сортировка по убыванию, тип -> бренд
type_list = ('Городской','Горный','Гоночный','Электро','BMX')
df = pd.read_sql(f'''
    SELECT id_bike AS ID, BrandBicycle.brand_name AS 'Бренд',ModelBicycle.name_model AS 'Модель',  TypeBicycle.type_name AS 'Тип', year_issue AS 'Год'
    FROM bike, ModelBicycle, BrandBicycle, TypeBicycle
    WHERE bike.id_model = ModelBicycle.id_model AND ModelBicycle.id_brand = BrandBicycle.id_brand
        AND BrandBicycle.id_type = TypeBicycle.id_type
        AND year_issue BETWEEN :p_year1 AND :p_year2 
    
                  AND type_name IN {type_list}
                  ORDER BY type_name ASC, brand_name ASC
''', con, params={"p_year1":2019,"p_year2":2022})
print(df)

print('2--------------------')

#Запрос на выборку информации о велосипеде, с указанием повреждения и общей суммы возмещенного ущерба.
#Сортировка по убыванию, модель
df = pd.read_sql(f'''
WITH get_tabl( id_b, id_br,model,dscrp,pr_dmg)
AS(
    SELECT b.id_bike AS id_b,br.idbike_rental AS id_br, mb.name_model AS model,
            rj.description ,rj.damage_sum AS price_dmg
    FROM bike b, ModelBicycle mb, rental_journal rj, bike_rental br
        WHERE b.id_bike = br.id_bike AND b.id_model = mb.id_model AND br.idbike_rental = rj.idbike_rental
    ORDER BY b.id_bike
    ),
get_cnt(id_b,id_br,model,dscrp,pr_dmg,cnt) AS
    (SELECT id_b,id_br,model,dscrp,pr_dmg, COUNT(id_b) AS cnt FROM get_tabl
    GROUP BY id_b),
 
get_id (id_b,id_br) AS   
    (SELECT id_b,id_br FROM get_cnt WHERE cnt>1),
    
get_id_br (id_br) AS
    (SELECT idbike_rental FROM bike_rental
    JOIN get_id ON id_b = bike_rental.id_bike),
    
get_sum_dmg(sm) AS
    (SELECT sum(damage_sum) FROM rental_journal
    JOIN get_id_br ON id_br = rental_journal.idbike_rental)
    
    SELECT id_b,id_br,model,dscrp,cnt, 
    CASE 
        WHEN cnt>1 
            THEN (SELECT sm FROM get_sum_dmg)
        ELSE pr_dmg
        END AS price FROM get_cnt
    WHERE price> :p_price
''', con,params={"p_price":3000})
print(df)

print('3-------------------')

# расчет чека с указанием цены за повреждения и сумму аренды
df = pd.read_sql(f'''
WITH 
get_rental (id_br,dmg_price) AS
    (SELECT br.idbike_rental,damage_sum 
     FROM bike_rental br
     LEFT JOIN rental_journal rj
     ON rj.idbike_rental = br.idbike_rental
     WHERE rj.idbike_rental IS NULL OR rj.idbike_rental IS NOT NULL),
     
get_price_type (id_b,id_br, type_pr)
AS (SELECT b.id_bike, idbike_rental AS id_br,price_type
    FROM bike b, ModelBicycle mb, BrandBicycle br, TypeBicycle tp, bike_rental
    WHERE b.id_model = mb.id_model AND mb.id_brand = br.id_brand AND br.id_type = tp.id_type AND bike_rental.id_bike = b.id_bike),

get_numeric (id_br, dmg_pr) AS
    (SELECT id_br,
     IIF(typeof(dmg_price)="integer", dmg_price, 0) AS dmg_price
     FROM get_rental )
     
SELECT type_pr*(julianday(date_return) - julianday(date_issue))+dmg_pr AS price, id_bike AS id_b, idbike_rental AS id_br,
  julianday(date_return) - julianday(date_issue) AS days,dmg_pr, type_pr AS tp_pr
  FROM bike_rental
  JOIN get_price_type ON get_price_type.id_br = bike_rental.idbike_rental
  JOIN get_numeric ON get_numeric.id_br = bike_rental.idbike_rental

''', con)
print(df)

print('4--------------------')

#Запрос на выборку информации о велосипеде, с указанием их количества на складе.
#Сортировка по убыванию,  название бренда, название модели
df = pd.read_sql(f'''
    SELECT brand_name,name_model,COUNT(b.id_model) AS amount
    FROM bike b, ModelBicycle mb, BrandBicycle bb
        WHERE b.id_model = mb.id_model AND mb.id_brand = bb.id_brand
    GROUP BY name_model  
    ORDER BY brand_name,name_model
''', con)
print(df)

print('5-------------------')

#Запрос на выборку информации о клиенте и количестве его заказов.
df = pd.read_sql(f'''    
    SELECT full_name,COUNT(idbike_rental) AS amount
    FROM bike_rental 
    JOIN client USING (id_client)
    GROUP BY full_name
    ORDER BY amount DESC
''', con)
print(df)

print('6-------------------')

df = pd.read_sql(f'''
    WITH get_popbike(id_b,amount_bike)
    AS (SELECT id_bike,COUNT(id_bike) AS amount_bike
        FROM bike_rental
        GROUP BY bike_rental.id_bike) 

SELECT name_model, id_bike, amount_bike AS popularity
    FROM bike
    JOIN get_popbike ON id_b = id_bike
    JOIN ModelBicycle USING (id_model)
ORDER BY popularity DESC

''', con)
print(df)

print('7-------------------')

date_regist = now.strftime("%Y-%m-%d")

print('Имя:')
full_name = input()
print('Телефон:')
phone_num = int(input())
print('Год рождения:')
year = int(input())
print('Месяц рождения:')
month = int(input())
print('День рождения:')
day = int(input())
date_birth = datetime.date(year,month,day)
cursor.execute("INSERT INTO client (full_name, phone_num,date_birth,date_regist) VALUES "
           "('{}', '{}', '{}', '{}') ".format( full_name, phone_num,date_birth,date_regist))
con.commit()

df = pd.read_sql(f'''    
    SELECT * FROM client
''', con)
print(df)

print('8-------------------')

print('ID:')
id_client = int(input())
cursor.execute("DELETE FROM client WHERE id_client = {}".format(id_client))
con.commit()
df = pd.read_sql(f'''    
    SELECT * FROM client
''', con)
print(df)
