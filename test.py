tables = {
    "vod_duration_proxy"    : "ds",
    "playtime_vod"          : "ds",
    "playtime_livetv"       : "ds",
    "vector_hour"           : "d",
    "vector_nation"         : "d",
    "vector_weekday"        : "d",
    "vector_cate"           : "d",
}
DATE = '2020-12-17'
addTable = ''

for table in tables.keys():
    stub = "ALTER TABLE dwh_fpt_play.{} ADD IF NOT EXISTS PARTITION ({}='{}') ; ".format(table, tables[table],DATE)
    addTable = addTable + stub

command = "beeline -n fplay -p dataengineerfpt2 -e \"{}\"".format(addTable)
print(command)