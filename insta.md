# INSTAGRAM BOT INFO

## ---- HOPS: 3 ---- initial list = 1 hop, then from that list it collects names for hop 2, then from that names for hop 3

**--------------------------------------------------------------------------------------------------------------------------------**

**Useful URLs:**
`https://i.instagram.com/api/v1/friendships/6048734544/followers/?count=12&max_id=12&search_surface=follow_list_page`
`https://i.instagram.com/api/v1/friendships/6048734544/following/?count=12`
`https://i.instagram.com/api/v1/media/2626242270782253644/comments/?can_support_threading=true&target_comment_id=17945982907519424&permalink_enabled=true`

**--------------------------------------------------------------------------------------------------------------------------------**

*Info we are getting for users:*
`external_url`
`full_name`
`edge_followed_by (count)`
`edge_follow (count)`
`id`
`highlight_reel_count`
`is_business_account`
`is_professional_account`
`category_enum`
`category_name`
`is_private`
`profile_pic_url`
`username`
`edge_owner_to_timeline_media (count)`
`is_verified`

**Info we need to get for users:**
`edge_followed_by (list)`
`edge_follow (list)`
`edge_owner_to_timeline_media (all posts)`

**--------------------------------------------------------------------------------------------------------------------------------**

*info we are getting for posts:*
`edge_media_to_tagged_user (list)`
`post_date`
`id`
`likes (count)`
`comments (count)`

**info we need to get for posts:**
`comments (list)`

**--------------------------------------------------------------------------------------------------------------------------------**

*info we are getting for comments:*
`id`

**info we need to get for comments:**
`comment date`
`user`
`comment content`
`likes (count)`
`tagged users info`

**--------------------------------------------------------------------------------------------------------------------------------**

*info we are getting for tagged user (in comments):*
`username`

**info we need to get for tagged user (in comments):**
`id`

**--------------------------------------------------------------------------------------------------------------------------------**

*info we are getting for replies (in comments):*
``

**info we need to get for replies (in comments):**
`username`
`id`
`count`
