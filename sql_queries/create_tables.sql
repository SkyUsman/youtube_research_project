----- TABLES FOR THE FILTERED AND NON-FILTERED COMMENTS.
DROP TABLE IF EXISTS Filtered_Comments;
DROP TABLE IF EXISTS All_Comments;

-- Note: author does not matter if nullable or not in our context.

CREATE TABLE Filtered_Comments (
    Unique_ID SERIAL PRIMARY KEY,
    Author TEXT NOT NULL,
    Comment TEXT NOT NULL,
    Likes INT NOT NULL,
    Published_At TIMESTAMP NOT NULL,
    Comment_ID TEXT NOT NULL,
    Survey_Yes BIGINT NULL,
    Survey_No BIGINT NULL,
    Survey_Skip BIGINT NULL
);

CREATE TABLE All_Comments (
    Unique_ID SERIAL PRIMARY KEY,
    Author TEXT NOT NULL,
    Comment TEXT NOT NULL,
    Likes INT NOT NULL,
    Published_At TIMESTAMP NOT NULL,
    Comment_ID TEXT NOT NULL
);
