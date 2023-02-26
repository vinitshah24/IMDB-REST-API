SELECT * FROM V$database;
SELECT * FROM user_tables;

SELECT object_name
FROM dba_objects
WHERE object_type = 'TABLE' AND owner = 'SYSTEM' AND created >= '24-FEB-2023';

SELECT * FROM SYSTEM.GENRE;
DESC SYSTEM.GENRE;

SELECT dbms_metadata.get_ddl('TABLE', 'GENRE', 'SYSTEM' ) FROM dual;

INSERT INTO SYSTEM.GENRE (GENRE_NAME) VALUES ('Horror');
INSERT INTO SYSTEM.GENRE (GENRE_NAME) VALUES ('Crime');
INSERT INTO SYSTEM.GENRE (GENRE_NAME) VALUES ('Action');
INSERT INTO SYSTEM.GENRE (GENRE_NAME) VALUES ('Drama');
SELECT * FROM SYSTEM.GENRE;
COMMIT;

alter session set "_ORACLE_SCRIPT"=true;
create user vinit identified by "vinit";
create user c##vinit identified by vinit;
GRANT CREATE SESSION TO c##vinit;
alter session set "_ORACLE_SCRIPT"=true;
grant create table to vinit;
GRANT CREATE PROCEDURE TO vinit;
GRANT CONNECT, CREATE SESSION TO vinit;
create user c##admin identified by admin;
alter session set "_ORACLE_SCRIPT"=true;
