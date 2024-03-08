-- ************************************** "public".users

CREATE TABLE IF NOT EXISTS "public".users
(
 "id"             integer NOT NULL,
 email          character NULL,
 gender         public NOT NULL,
 password_hash  character NULL,
 created_at     timestamp NULL,
 last_logged_in timestamp NULL,
 CONSTRAINT users_pkey PRIMARY KEY ( "id" )
);
