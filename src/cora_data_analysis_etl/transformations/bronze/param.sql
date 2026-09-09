-- a real .sql file in your pipeline's source directory, e.g. bronze/_param_bridge.sql
CREATE OR REFRESH MATERIALIZED VIEW fort63_file_keys_param AS
SELECT :fort63_file_keys AS file_keys_json;