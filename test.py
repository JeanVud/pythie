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
#print(command)





add_hive_partitions = []
tables = {
    'play_stats_proxy_kafka'    : '/data/fplay/warehouse/play_stats_proxy_kafka',
    'play_stats_proxy_kafka2'   : '/data/fplay/warehouse/play_stats_hourly',
    'play_stats_proxy'          : '/data/fplay/warehouse/play_stats_proxy_refactor',
    'play_stats'                : '/data/fplay/warehouse/play_stats_refactor'
}
for table, path in tables.items():
    bash_command = 'sh /projects/fplay/scripts/fplay_add_hive_partitions.sh {} {}'
    add_hive_partitions.append(BashOperator(
        task_id='add_hive_partition_to_table_{}'.format(table),
        bash_command=bash_command.format(table,path),
        run_as_user='fplay',
        dag=dag
    ))


