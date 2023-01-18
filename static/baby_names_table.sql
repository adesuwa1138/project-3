-- Drop table if exists
DROP TABLE baby_names;

-- Create new table
CREATE TABLE "baby_names" (
	"Year" INT  NOT NULL,
	"Sex" VARCHAR(6)  NOT NULL,
	"Rank" INT  NOT NULL,
	"Name" VARCHAR(15)  NOT NULL,
	"Count" INT  NOT NULL,
	"Data_Revision_Date" DATE  NOT NULL);
	
-- View table columns and datatypes
SELECT * FROM baby_names;