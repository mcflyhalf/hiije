> This contains instructions on how to setup hiije for the very first time.

To start with, you will need your file with historical transactional data in some appropriate text based format (csv, txt etc). You will also need to have installed a RDBMS such as Postgres or MySQL. In this guide, Postgres is used along with a csv file.

%%For this description of steps, it would be graphically very cool if you drew a tree to show the progression of steps and at some point these steps branch into testing setup and usage setup. Because some things need only be done for testing params and others need to be doe only when actually setting up for usage.%%

In a high level, the things that need to be done are:
- Create a database to be used (done using the RDBMS)
- Find the unique items in the historical transactions and give each unique item a UID. In this case it is done according to decreasing popularity such that the most frequently appearing item is given the UID 1 and the least frequently occurring item is given the last UID
- For efficiency, remove all transactions that contain only 1 item (these are not useful for predictions)
- Divide your transactions into a training and test set. (The test set is usually a small percentage of the total data e.g you could use 95% of the data for training and 5% for testing. In a previous dataset, the training-test ratio that gave the best performance was 90%-10%. Which ratio to use really depends only on the particular dataset and hence can only be known by actually testing i.e dividing it in a particular proportion, testing the performance of that proportion and then dividing into another proportion and testing again. Doing this for 5, 10, 15, 20, 25 and 30% test ste sizes should yield a graph (test performance vs test set size) which peaks at the optimum value of test vs training partition)
- Commit your training set into the database in a binary format. This format is useful for quick access and also will speed up computation later on.
- Compute the Item-Item similarity matrix on your training database. This is the only step that takes a long time. For a training set of about 8500 transactions, this step took around 20 minutes on my core i3, 2.7 GHz machine. Thankfully, this step need only be done a few times when doing the initial setup.
- At this point, it is possible to determine the performance of the current similarity matrix by testing it against all transactions in the test set. A typical test would involve, for each test transaction, hide one of the items in the transaction(at random) and then present the other item to the recommender. If it correctly guesses the hidden item, this is considered a hit, if it doesnt, this is a miss. The performance may then be given as a ratio of hits/(hits+misses).
- If the performance is satisfactory, the recommender may then be deployed to offer recommendations

Each of the steps above is described in detail below.

### Create a database to be used (done using the RDBMS)
This is rather simple. On your favourite RDBMS, execute the command to create a database. In a Linux-Postgres combination, go to your terminal and execute the command ```createdb DBNAME``` where ```DBNAME``` is the name of the database you would like to create. In this example, I am going to be using a database called ```hiije_supermarket```. In case your Postgres is freshly installed, you may need to create a new database to be able to use Postgres from your terminal without having to change to the postgres user who is usually added along with the postgres installation. In case this last statement about users doesnt make sense, see this [explanation of how users and aceess works](https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps--2) in the Postgres-Linux combination. My suggestion is that you create a DB for your usual Linux user and another Postgres user (and not a user on your OS) for the user you will use. This second user doesnt require superuser privileges. Then log in as this second user using the loopback network interface (appearing as if the connection is originating from outside your local machine) using the command:
```psql -U username -d DBname -h 127.0.0.1 -W```
Using this command, it is possible to log in using the user you just created.

### Find the unique items in the historical transactions and give each unique item a UID
To do this, run the file ```create_item_ID_file.py```. This file requires 2 inputs(which should be in the same directory)- ```item_occurence_count3.py``` and your training dataset which in this case we will call ```training_data.csv```. The prompt
```How many unique items should be in the database(-1 for max)?-->  ```
should then appear. Let this number be k. If k is less than 0 (e.g -1), then all unique items will be captured, if k is a number greater than 1, then the top k most popular items will be captured. If in doubt, just set k to -1. The final output should be a file called ```item_ID.txt```.

### For efficiency, remove all transactions that contain only 1 item (these are not useful for predictions)
> Will do later

### Divide your transactions into a training and test set
> Will do later

### Commit your training set into the database in a binary format
