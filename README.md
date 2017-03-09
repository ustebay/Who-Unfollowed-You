# Who unfollowed you on Twitter?

This is a small project I did while playing around with the Twitter API. You can use it to compare the Twitter followers over time, or between different accounts. So for example run 
python find_followers.py userName > followers_day1.txt
on day 1 and run it again on day 2, 
python find_followers.py userName > followers_day2.txt
Then you can see which Twitter accounts unfollowed you from day 1 to day 2:
`python whoUnfollowed.py followers_day1 followers_day2`

Of course, if you input the new file first, then you will get the list of new followers:
python whoUnfollowed.py followers_day1 followers_day2

Or compare two accounts by:
python find_followers.py userName1 > followers_userName1.txt
python find_followers.py userName2 > followers_userName2.txt
python whoUnfollowed.py followers_userName1 followers_userName2

Note that I removed my Twitter developer credentials from the files, you need to enter yours to make this run. Enjoy!