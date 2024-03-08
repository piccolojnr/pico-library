-- ************************************** "public".book_languages

CREATE TABLE IF NOT EXISTS "public".book_languages
(
 book_id     integer NOT NULL,
 language_id character NOT NULL,
 CONSTRAINT book_languages_pkey PRIMARY KEY ( book_id, language_id ),
 CONSTRAINT book_languages_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_languages_language_id_fkey FOREIGN KEY ( language_id ) REFERENCES "public".languages ( code ) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "public".languages
(
 code character NOT NULL,
 CONSTRAINT languages_pkey PRIMARY KEY ( code )
);

