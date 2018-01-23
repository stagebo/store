DROP TABLE IF EXISTS t_jieba;
CREATE TABLE t_jieba (
  f_time datetime NOT NULL,
  f_content text NOT NULL,
  f_ip nvarchar(64),
  f_city nvarchar(256)
)

DROP TABLE IF EXISTS t_comment;
CREATE TABLE t_comment(
f_id nvarchar(64) primary keys not null,
f_root_id nvarchar(64),
f_pid nvarchar(64),
f_time datetime,
f_user_id nvarchar(64),
f_user_type smallint,
f_content text

)