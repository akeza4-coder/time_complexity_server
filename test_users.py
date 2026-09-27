def deduplicate_users(users):
    seen_ids = set()
    unique_users = []
    for user in users:
        uid = user['id']
        if uid not in seen_ids:
            seen_ids.add(uid)
            unique_users.append(user)
    return unique_users

# Test it with some sample data:
sample_users = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 2}]
result = deduplicate_users(sample_users)
print(result)