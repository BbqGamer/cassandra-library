## Stress tests
After writing tests utilizing concurrency I ran into the following problem: 
multiple reservations were created for the same book

#### Test 1 partial results
```
364bac5a-b005-478f-af24-899060af980d - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by tester@gmail.com
4d427ab1-f87d-43e3-850c-db987a728fde - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by tester@gmail.com
522485ec-56e3-4a38-9006-8822914a15e5 - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by tester@gmail.com
...
```

#### Test 2 partial results
```
295f31c8-ef7b-4865-804b-bddda400c2eb - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by second@test.com
df24ec03-2025-46c2-938b-b25b265faa52 - Killers of the Flower Moon: The Osage Murders and the Birth of the FBI - reserved by second@test.com
ca40d808-e504-4ef7-8c40-00f68e243a38 - Origin: A Novel (Robert Langdon) - reserved by first@test.com
09392399-3200-4758-a7ff-8fee1ec138b9 - The Life-Changing Magic of Tidying Up: The Japanese Art of Decluttering and Organizing - reserved by first@test.com
ab0cd372-0a95-4a8b-846d-d07b351014e9 - The Martian - reserved by second@test.com
d0c1b0b0-f6b0-41ce-b879-78fe458d43cc - The Martian - reserved by first@test.com
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
