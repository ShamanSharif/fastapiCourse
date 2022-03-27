select * from pg_catalog.pg_tables;

drop table test;

create table test (
    name varchar(40)
);

select * from test;

CREATE TABLE products (
    name varchar(255) not null,
    price integer not null,
    id serial primary key
);

SELECT * FROM products;

INSERT INTO products(name, price, on_sale, inventory)
VALUES ('Vivo V23', 34000, true, 5);

ALTER TABLE products ADD COLUMN
on_sale boolean default false;

ALTER TABLE products ADD COLUMN
inventory smallint not null default 0;

ALTER TABLE products ADD COLUMN
creaetd_at timestamp with time zone default now();

INSERT INTO products (name, price, on_sale, inventory) VALUES ('iPad 9 WiFi', 41000, true, 14);

SELECT * FROM products WHERE products.inventory = 0;

DELETE FROM products where id = 1;

INSERT INTO products (name, price) VALUES ('Realme 9 Pro+', 35000) RETURNING *;

UPDATE products SET on_sale = true WHERE id = 4;

SELECT * FROM products;