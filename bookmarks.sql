-- ************************************** "public".bookmarks

CREATE TABLE IF NOT EXISTS "public".bookmarks
(
 user_id    integer NOT NULL,
 book_id    integer NOT NULL,
 status     public NULL,
 last_read  timestamp NOT NULL,
 created_at timestamp NULL,
 CONSTRAINT bookmarks_pkey PRIMARY KEY ( user_id, book_id ),
 CONSTRAINT bookmarks_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT bookmarks_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);

