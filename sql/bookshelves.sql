-- ************************************** "public".book_bookshelves

CREATE TABLE "public".book_bookshelves
(
 book_id      integer NOT NULL,
 bookshelf_id integer NOT NULL,
 CONSTRAINT book_bookshelves_pkey PRIMARY KEY ( book_id, bookshelf_id ),
 CONSTRAINT book_bookshelves_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_bookshelves_bookshelf_id_fkey FOREIGN KEY ( bookshelf_id ) REFERENCES "public".bookshelves ( "id" ) ON DELETE CASCADE
);

-- ************************************** "public".bookshelves

CREATE TABLE IF NOT EXISTS "public".bookshelves
(
 "id"   integer NOT NULL,
 name character NULL,
 CONSTRAINT bookshelves_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT bookshelves_name_key UNIQUE ( name )
);
