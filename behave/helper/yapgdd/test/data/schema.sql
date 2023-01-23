CREATE TABLE [personal_details] (
  [full_name] TEXT,
  [age] INT,
  [address] TEXT,
  [postcode] TEXT,
  [created] TEXT
);

INSERT INTO [personal_details] VALUES
('John smith',35,'123 fake street','SW1','2023-01-11 14:45:46.149383+00');


CREATE TABLE [logs] (
  [id] INT,
  [code] TEXT,
  [level] INT,
  [created] TEXT
);
