-- ************************************** "public".ratings

CREATE TABLE IF NOT EXISTS "public".ratings
(
 user_id integer NOT NULL,
 book_id integer NOT NULL,
 rating  double NULL,
 CONSTRAINT ratings_pkey PRIMARY KEY ( user_id, book_id ),
 CONSTRAINT ratings_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT ratings_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);