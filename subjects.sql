-- ************************************** "public".book_subjects

CREATE TABLE IF NOT EXISTS "public".book_subjects
(
 book_id    integer NOT NULL,
 subject_id integer NOT NULL,
 CONSTRAINT book_subjects_pkey PRIMARY KEY ( book_id, subject_id ),
 CONSTRAINT book_subjects_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT book_subjects_subject_id_fkey FOREIGN KEY ( subject_id ) REFERENCES "public".subjects ( "id" ) ON DELETE CASCADE
);


-- ************************************** "public".subjects

CREATE TABLE IF NOT EXISTS "public".subjects
(
 "id"   integer NOT NULL,
 name character NULL,
 CONSTRAINT subjects_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT subjects_name_key UNIQUE ( name )
);




