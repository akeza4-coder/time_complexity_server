users = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 2}]

seen_ids = set()
unique_users = []

for user in users:
    user_id = user['id']
    if user_id not in seen_ids:
        seen_ids.add(user_id)
        unique_users.append(user)

print(unique_users)