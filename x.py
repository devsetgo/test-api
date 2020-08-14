
where_list = []

add_to_where = [(detail_table.c.col1, 3), (detail_table.c.col2, 5)]


for a in add_to_where:
    print(a)


