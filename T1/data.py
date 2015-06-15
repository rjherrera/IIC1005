import json
import random

f = open('raw_data/foursquare_checkins.csv')
f.readline()  # primera linea es de información extra
everything = f.readlines()
f.close()
checkins_number = len(everything)

checkins = [line.strip().split(',') for line in everything]
locations = [line[-1] for line in checkins]
users = [line[0] for line in checkins]

users_number = len(list(set(users)))
locations_number = len(list(set(locations)))
average_check_ins_per_user = checkins_number / users_number
average_check_ins_per_location = checkins_number / locations_number

f = open('raw_data/foursquare_friendship.csv')
f.readline()  # primera linea info innecesaria
friendships = f.readlines()
f.close()
friendships_number = len(friendships)
average_friends_per_user = friendships_number / users_number

data = {'check_ins': checkins_number, 'users': users_number, 'locations': locations_number,
        'average_check_ins_per_user': round(average_check_ins_per_user, 1),
        'average_check_ins_per_location': round(average_check_ins_per_location, 1),
        'average_friends_per_user': round(average_friends_per_user, 1)}

with open('processed_data/info.json', 'w') as outfile:
    json.dump(data, outfile)

print('Basic information file created. Saved in processed_data/info.json')

random_500 = random.sample(checkins, 500)
for i in random_500:
    i[1] = float(i[1])
    i[2] = float(i[2])
string = 'var locations = ' + str(random_500)
f = open('processed_data/random_500.js', 'w')
f.write(string)
f.close()
print('Random locations file created. Saved in processed_data/random_500.js')
