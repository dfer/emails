-- Drop all objects in db
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS log;

DROP INDEX IF EXISTS message_created_idx;
DROP INDEX IF EXISTS message_int_id_idx;
DROP INDEX IF EXISTS log_address_idx;
