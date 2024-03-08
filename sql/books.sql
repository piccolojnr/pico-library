-- ************************************** "public".books

CREATE TABLE IF NOT EXISTS "public".books
(
 "id"           integer NOT NULL,
 "format"       character NULL,
 title        character NULL,
 description  text NULL,
 downloads    integer NULL,
 license      character NULL,
 date_created timestamp NULL,
 CONSTRAINT books_pkey PRIMARY KEY ( "id" )
);






