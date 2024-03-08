-- ************************************** "public".comment_votes

CREATE TABLE IF NOT EXISTS "public".comment_votes
(
 "id"         integer NOT NULL,
 vote_type  public NULL,
 created_at timestamp NULL,
 updated_at timestamp NULL,
 comment_id integer NULL,
 user_id    integer NULL,
 CONSTRAINT comment_votes_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT comment_votes_comment_id_fkey FOREIGN KEY ( comment_id ) REFERENCES "public".comments ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comment_votes_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);


-- ************************************** "public".comments

CREATE TABLE IF NOT EXISTS "public".comments
(
 "id"         integer NOT NULL,
 content    text NULL,
 created_at timestamp NULL,
 updated_at timestamp NULL,
 book_id    integer NULL,
 user_id    integer NULL,
 parent_id  integer NULL,
 review_id  integer NULL,
 CONSTRAINT comments_pkey PRIMARY KEY ( "id" ),
 CONSTRAINT comments_book_id_fkey FOREIGN KEY ( book_id ) REFERENCES "public".books ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comments_parent_id_fkey FOREIGN KEY ( parent_id ) REFERENCES "public".comments ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comments_review_id_fkey FOREIGN KEY ( review_id ) REFERENCES "public".reviews ( "id" ) ON DELETE CASCADE,
 CONSTRAINT comments_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".users ( "id" ) ON DELETE CASCADE
);
