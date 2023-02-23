INSERT INTO [logs] VALUES
(1,'CASE_CREATED',29,'2023-01-17 15:49:46.149383+00'),
(1,'DIAGNOSIS_CREATED',29,'2023-01-17 15:48:46.149383+00'),
(1,'COMPLAINT_CREATED',29,'2023-01-17 15:47:46.149383+00');

INSERT INTO [personal_details] VALUES
('John smith',35,'123 fake street','SW1','2023-01-11 14:45:46.149383+00');

-- This is testing removing a column from the target database
ALTER TABLE [status] DROP COLUMN 'code';
INSERT INTO [status] VALUES
(1,'NEW','2023-01-18 15:43:46.149383+00');