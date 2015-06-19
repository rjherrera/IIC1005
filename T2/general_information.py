import MySQLdb as sql  # change to cymysql if needed (same syntax)


def count_rows(cursor, column, table, distinct=False):
    query = ('SELECT COUNT(%s%s) FROM %s;' % ('DISTINCT ' if distinct else '', column, table))
    cursor.execute(query)
    return cursor.fetchone()[0]

db = sql.connect(host='localhost',
                 user='user',
                 passwd='',
                 db='iic1005')

cur = db.cursor()

users = count_rows(cur, 'id', 'about', distinct=True)
stores = count_rows(cur, 'store_id', 'stores', distinct=True)
categories = count_rows(cur, 'category', 'categories', distinct=True)
products = count_rows(cur, 'product_id', 'products', distinct=True)
print(products)
reviews = count_rows(cur, 'reviews.product_id',
                           'reviews JOIN products ON products.product_id = reviews.product_id')
product_comments = count_rows(cur, 'products.product_id',
                               'products JOIN (comments JOIN reviews ON comments.rid = reviews.id) ON products.product_id = reviews.product_id;')

loves = count_rows(cur, 'type', 'feed WHERE type = "LOVE"')
comments_feed = count_rows(cur, 'type', 'feed WHERE type = "COMMENT"')
wallposts = count_rows(cur, 'type', 'feed WHERE type = "WALLPOST"')
snapshots = count_rows(cur, 'type', 'feed WHERE type = "SNAPSHOT"')

print('Número de usuarios:', users)
print('Número de tiendas:', stores)
print('Número de categorias de productos:', categories)
print('Número promedio de:')
print('  Reviews por producto:', reviews / products)
print('  Comments por producto:', product_comments / products)
print('  Loves por usuario:', loves / users)
print('  Comments por usuario:', comments_feed / users)
print('  Wallposts por usuario:', wallposts / users)
print('  Snapshots por usuario:', snapshots / users)
