## Item Based Collaborative Filters
This doc aims to describe what an item-based collaborative filter is. It aims to do so without invoking any complex mathematics. It only explores the logic behind all the working.

### The Problem
An easy way to understand what Item Based collaborative filters are, is to first understand what problem they were created to solve. The basic problem is recommendation. That is, if a certain person in a supermarket has bought item _a_ and item _b_, how can we find another item _c_ that will also interest the person. This same problem arises in recommending videos on YouTube, dates on Tinder, songs on itunes, news articles on Google news among many other scenarios.
There are a few methods that have been proposed and item based collaborative filters are one of the proposed methods.

### The solution
To walk through the solution, consider a user on itunes. This user owns a few songs and we seek to find other songs that might interest him. To do this, we might look at particular properties of the songs that this user has and recommend other songs that have the highest combinations of these properties. The properties we may look at include the singers of the song, the genre, the nature (collaboration or single), the tempo, the album, the year of production etc. We would then look through the other songs on iTunes and find other songs that have similar characteristics that the user does not already have and then recommend these to the user. This is the essence of how collaborative filters work.
