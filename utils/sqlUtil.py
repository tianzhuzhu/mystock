def getsql(sql_path):
    sql = open(sql_path, "r", encoding="utf8")
    sql = sql.readlines()
    sql = "".join(sql)
    return sql