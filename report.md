## Synchronization Problems
After writing stress tests utilizing concurrency I ran into the following problem: 
multiple reservations were created for the same book

#### Test 1 partial results
```
364bac5a-b005-478f-af24-899060af980d - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by tester
4d427ab1-f87d-43e3-850c-db987a728fde - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by tester
522485ec-56e3-4a38-9006-8822914a15e5 - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by tester
...
```

#### Test 2 partial results
```
295f31c8-ef7b-4865-804b-bddda400c2eb - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by bar
df24ec03-2025-46c2-938b-b25b265faa52 - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by bar
ca40d808-e504-4ef7-8c40-00f68e243a38 - Origin: A Novel (Robert Langdon) - reserved by foo
09392399-3200-4758-a7ff-8fee1ec138b9 - The Life-Changing Magic of Tidying Up: The Japanese Art of Decluttering and Organizing - reserved by foo
ab0cd372-0a95-4a8b-846d-d07b351014e9 - The Martian - reserved by bar
d0c1b0b0-f6b0-41ce-b879-78fe458d43cc - The Martian - reserved by foo
...
```

### Test 3 partial results
```
878da01c-e5d4-4d2b-8b5b-fffd8d5e8ac3 - The 5 Love Languages: The Secret to Love That Lasts - reserved by bar
d255d537-7814-4f87-9d70-1fbabdca6048 - The 5 Love Languages: The Secret to Love That Lasts - reserved by foo
507291a9-0dc6-406f-8e57-9c5a792ec357 - The Hunger Games (Book 1) - reserved by foo
b1ccd76d-c982-4000-9190-d887aaa439d4 - The Hunger Games (Book 1) - reserved by bar
...
```

### Fix
I used lightweight transactions to fix this problem. 
`INSERT INTO library.reservations_by_book (book_id, id, email) VALUES (%s, %s, %s) IF NOT EXISTS`
`book_id` is primary key in this table and this query fails if there is already some record
with this `book_id`. We can check if it was successfull with property `was_applied` of the
result of the query. This was enough to fix test 1 and test 2:

### Test 1 whole results
This time I only received one row (as expected) the whole test takes around 20 seconds
```
e7b49fc1-c5fd-4bba-841b-331936ca8c76 - National Geographic Little Kids First Big Book of Why (National Geographic Little Kids First Big Books) - reserved by tester
```

### Test 2 partial resuls
Second test was also fixed, we can see mix of the users in the reservations (they made a lot of random requests)
```
4ef40565-6183-4b76-afe7-31b3a5cf5473 - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by foo
d132ecaa-7f0c-40b8-9ce8-8467042579b9 - JOURNEY TO THE ICE P - reserved by foo
5ffbc8da-17d1-4630-967e-7aa019af0a10 - The Nightingale: A Novel - reserved by bar
7e616a17-310a-46ba-ad45-c4732c5e1c5b - Pokémon Deluxe Essential Handbook: The Need-to-Know Stats and Facts on Over 700 Pokémon - reserved by foo
c3eb1f0e-6a9f-4a80-bd1f-f9eca4a7366d - Uninvited: Living Loved When You Feel Less Than, Left Out, and Lonely - reserved by bar
...
```

### Test 3 partial results
Third test also worked, now both parties get roughly the same number of reservations (non takes all)
```
9106cbc0-2f17-4b65-8af7-906b287cfe63 - The Book Thief - reserved by bar
c4936b37-77cb-4616-b196-de889832c3df - Option B: Facing Adversity, Building Resilience, and Finding Joy - reserved by foo
42146ab7-0528-4179-9022-c48563be2afa - Goodnight, Goodnight Construction Site (Hardcover Books for Toddlers, Preschool Books for Kids) - reserved by foo
abc87f73-c491-4546-8f09-f2505257eff9 - The Life-Changing Magic of Tidying Up: The Japanese Art of Decluttering and Organizing - reserved by bar
...
```
Also I needed to count only the reservations that succedeed to show number of books reserved to the user:
```
success = db.add_new_reservation(key, user_email)
if success:
    reserved += 1
```

 
