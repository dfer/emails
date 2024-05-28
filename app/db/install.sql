-- Create the 'message' table
CREATE TABLE IF NOT EXISTS message (
    created TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    id VARCHAR NOT NULL,
    int_id CHAR(16) NOT NULL,
    str VARCHAR NOT NULL,
    status BOOL,
    CONSTRAINT message_id_pk PRIMARY KEY(id)
);

-- Create indexes on the 'message' table
CREATE INDEX IF NOT EXISTS message_created_idx ON message (created);
CREATE INDEX IF NOT EXISTS message_int_id_idx ON message (int_id);

-- Create the 'log' table
CREATE TABLE IF NOT EXISTS log (
    created TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    int_id CHAR(16) NOT NULL,
    str VARCHAR,
    address VARCHAR
);

-- Create a hash index on the 'log' table using the 'address' column
CREATE INDEX IF NOT EXISTS log_address_idx ON log USING hash (address);
