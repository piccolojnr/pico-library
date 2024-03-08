-- ************************************** "public".profile

CREATE TABLE IF NOT EXISTS "public".profile
(
 "id"            integer NOT NULL,
 user_id       integer NULL,
 full_name     character NULL,
 bio           text NULL,
 occupation    character NULL,
 location      character NULL,
 profile_image character NULL,
 created_at    timestamp NULL,
 CONSTRAINT profile_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT profile_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);


