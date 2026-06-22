Update website/README.blog.md by

1) Run the script `website/find_published_blogs.sh` to update the list of `## Published Blogs`

2) Create a table of all the draft blogs in `website/docs/blog/posts/draft*`
- Write the result in a markdown table with columns
  - File: with full path (e.g., `website/docs/blog/posts/draft.in_10_mins.helpers_open_md.md`)
  - Number of Words
  - Ready %: in 0 to 100%
  - Comment: less than 50 chars on what needs to be done to get it to 100%
- Rank them from how close they are to be publishable
