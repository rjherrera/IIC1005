import MySQLdb as sql
from textblob import TextBlob
import datetime
import numpy as np
import csv


def select_table_rows(cursor, table):
    query = "SELECT * from `%s`" % (table)
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def count_feed_types_per_user(cursor, value):
    query = ("""SELECT `type`, count(`type`) as CountOf
                 from (SELECT `type`,`source` from `feed` WHERE `source` = '%s') as `feed`
                group by `type` """  % (value))
    cursor.execute(query)
    if cursor.rowcount > 0:
        return cursor.fetchall()
    return []


def is_seller(cursor, value):
    query = ("""SELECT 'SELLER', 1 FROM sellers WHERE `name` = '%s'"""
             % (value))
    cursor.execute(query)
    if cursor.rowcount > 0:
        return cursor.fetchall()
    return []


def in_out_degree_per_user(cursor, value):
    query1 = ("""SELECT 'IN_DEGREE', count(type)
                 from (SELECT type, destination from feed
                       WHERE destination='%s' and source != '%s')
                       as feed
             """ % (value, value))
    query2 = ("""SELECT 'OUT_DEGREE', count(type)
                 from (SELECT type, source from feed WHERE  source = '%s' and destination !='%s')
                       as feed
             """ % (value, value))
    cursor.execute(query1)
    in_deg = cursor.fetchall()
    cursor.execute(query2)
    out_deg = cursor.fetchall()
    return [(in_deg[0][0], in_deg[0][1]), (out_deg[0][0], out_deg[0][1])]


def select_specific_column_values(cursor, table, col, col_2, value, suffix):
    query = ("""SELECT %s from %s WHERE %s = '%s';"""
             % (col, table, col_2, value))
    cursor.execute(query)
    if cursor.rowcount > 0:
        data = cursor.fetchall()
        data_sub = [(TextBlob(x[0]).sentiment.subjectivity) for x in data]
        data_pol = [(TextBlob(x[0]).sentiment.polarity) for x in data]
        return [('AVG_SUB' + suffix, np.average(data_sub)), ('STD_SUB' + suffix, np.std(data_sub)),
                ('AVG_POL' + suffix, np.average(data_pol)), ('STD_POL' + suffix, np.std(data_pol))]
    return []


db = sql.connect(host='localhost', user='root', passwd='', db='iic1005')
cursor = db.cursor()
rows = select_table_rows(cursor, 'about')

a = datetime.datetime.now()  # Starting time
i = 0  # Inside loop counter
info_users = []
fieldnames = ["AVATAR",
              "SELLER", "SNAPSHOT", "COMMENT", "WALLPOST", "LOVE", "IN_DEGREE", "OUT_DEGREE",
              "AVG_SUB_COM_MAR", "AVG_POL_COM_MAR", "STD_SUB_COM_MAR", "STD_POL_COM_MAR",
              "AVG_SUB_REV_MAR", "AVG_POL_REV_MAR", "STD_SUB_REV_MAR", "STD_POL_REV_MAR",
              "AVG_SUB_COM_SOC", "AVG_POL_COM_SOC", "STD_SUB_COM_SOC", "STD_POL_COM_SOC",
              "AVG_SUB_STA_SOC", "AVG_POL_STA_SOC", "STD_SUB_STA_SOC", "STD_POL_STA_SOC"]

for row in rows:
    user = {"AVATAR": row[1], "SELLER": 0, "SNAPSHOT": 0,
            "COMMENT": 0, "WALLPOST": 0, "LOVE": 0, "IN_DEGREE": 0, "OUT_DEGREE": 0}
    for field in fieldnames[7:]:
        user[field] = 0
    dataset1 = count_feed_types_per_user(
                            cursor,
                            row[1])
    dataset2 = in_out_degree_per_user(
                            cursor,
                            row[1])
    dataset3 = select_specific_column_values(
                            cursor, 'feed', 'data',
                            'source', row[1] + "' and `type` = 'COMMENT",
                            '_COM_SOC')
    dataset4 = select_specific_column_values(
                            cursor, 'feed', 'data',
                            'source', row[1] + "' and `type` = 'WALLPOST",
                            '_STA_SOC')
    dataset5 = select_specific_column_values(
                            cursor,
                            'reviews JOIN products ON products.product_id = reviews.product_id',
                            'review', 'name', row[1], '_REV_MAR')
    dataset6 = select_specific_column_values(
                            cursor,
                            'comments',
                            'comment', 'comments.name', row[1], '_COM_MAR')
    dataset7 = is_seller(cursor, row[1])

    datasets = [dataset1, dataset2, dataset3, dataset4, dataset5, dataset6, dataset7]
    for dataset in datasets:
        for data in dataset:
            user[data[0]] = data[1]
    info_users.append(user)
    i += 1
    if i in range(50, 4000, 200):  # Visual Counter
        print('.')
    if i in range(100, 4000, 200):
        print('..')
    if i in range(150, 4000, 200):
        print('...')
    if i % (200) == 0:
        print(str(i*100/4000) + '%')
    if i % 4000 == 0:
        break

b = datetime.datetime.now()  # Finish time
print(b - a)  # Timing!

with open('dataset.csv', "w") as csvfile:
    reader = csv.DictWriter(csvfile, fieldnames=fieldnames)
    reader.writeheader()
    reader.writerows(info_users)

# Query Graveyard
    # old FROM market comments:
    # 'comments JOIN reviews ON comments.rid = reviews.id) ON products.product_id = reviews.product_id',
    #
    # old in out degree query:
    # query = ("""SELECT 'OUT_DEGREE', Case when source = '%s' then count(type) else 0 end,
    #                    'IN_DEGREE', Case when destination = '%s' then count(type) else 0 end
    #              from (SELECT type,source,destination from feed
    #                    WHERE  source = '%s' or destination='%s' HAVING source != destination)
    #                    as feed
