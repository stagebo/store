DROP TABLE IF EXISTS t_jieba;
CREATE TABLE t_jieba (
  f_time datetime NOT NULL,
  f_content text NOT NULL,
  f_ip nvarchar(64),
  f_city nvarchar(256)
)