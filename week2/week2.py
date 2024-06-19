import praw
from collections import defaultdict

# Reddit API credentials
client_id = 'private'
client_secret = 'private'
user_agent = 'datahw'

# Authenticate with Reddit
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Choose a subreddit and time period
subreddit = reddit.subreddit('learnprogramming')
posts = subreddit.top(time_filter='month', limit=100)

# Initialize data structures
user_connections = defaultdict(set)
user_flair = {}

# Collect data
for post in posts:
    post.comments.replace_more(limit=0)
    for comment in post.comments.list():
        if comment.author:  # Check if comment.author is not None
            user = comment.author.name
            flair = comment.author_flair_text or "Unknown"
            user_flair[user] = flair
            for reply in comment.replies:
                if reply.author:  # Check if reply.author is not None
                    replier = reply.author.name
                    user_flair[replier] = reply.author_flair_text or "Unknown"
                    user_connections[user].add(replier)
                    user_connections[replier].add(user)

# Calculate degree centrality
degree_centrality = {user: len(connections) for user, connections in user_connections.items()}

# Group users by flair and analyze centrality
flair_centrality = defaultdict(list)
for user, centrality in degree_centrality.items():
    flair = user_flair.get(user, 'Unknown')
    flair_centrality[flair].append(centrality)

# Calculate average centrality for each flair
average_centrality = {flair: sum(centralities) / len(centralities) for flair, centralities in flair_centrality.items()}

# Output results
for flair, avg_centrality in average_centrality.items():
    print(f"Average Degree Centrality for {flair}: {avg_centrality:.2f}")
