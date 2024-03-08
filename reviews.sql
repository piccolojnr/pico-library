-- ************************************** "public".reviews

CREATE TABLE IF NOT EXISTS "public".reviews
(
 "id"         integer NOT NULL,
 title      character NOT NULL,
 review     character NOT NULL,
 book_id    integer NOT NULL,
 user_id    integer NOT NULL,
 created_at timestamp NULL,
 CONSTRAINT reviews_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT reviews_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT reviews_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);




