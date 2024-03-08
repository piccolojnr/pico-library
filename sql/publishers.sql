-- ************************************** "public".book_publishers

CREATE TABLE IF NOT EXISTS "public".book_publishers
(
 book_id      integer NOT NULL,
 publisher_id character NOT NULL,
 CONSTRAINT book_publishers_pkey PRIMARY KEY ( book_id, publisher_id ),
 CONSTRAINT book_publishers_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_publishers_publisher_id_fkey FOREIGN KEY ( publisher_id ) REFERENCES "public".publishers ( name ) ON DELETE CASCADE
);


-- ************************************** "public".publishers

CREATE TABLE IF NOT EXISTS "public".publishers
(
 name character NOT NULL,
 CONSTRAINT publishers_pkey PRIMARY KEY ( name )
);
