
create table amazon
(
    id int auto_increment
        primary key,
    created_at datetime default now() not null,
    title varchar(1000) null,
    link varchar(1000) null,
    image varchar(1000) null,
    price varchar(100) null,
    stars varchar(50) null,
    prime varchar(1000) null,
    raters varchar(50) null
);

create table scraping.ebay
(
    id int auto_increment
        primary key,
    created_at datetime default now() not null,
title varchar(1000) null,
link varchar(1000) null,
image varchar(1000) null,
price varchar(100) null,
discount varchar(300) null
);
--
--         res.append({
--             'subreddit': post.subreddit.display_name,
--             'advertiser_category': post.subreddit.advertiser_category,
--             'author': post.author.fullname,
--             'total_karma': post.author.total_karma,
--             'score': post.score,
--             'title': post.title,
--             'ups': post.ups,
--             'upvote_ratio': post.upvote_ratio,
--             'selftext': post.selftext,
--             'thumbnail': post.thumbnail,
--             'domain': post.domain,
--             'created': post.created
--
--         })

create table scraping.reddit
(
    id int auto_increment
        primary key,
    created_at datetime default now() not null,
    subreddit varchar(300) null,
    advertiser_category varchar(300) null,
    author varchar(200) null,
    total_karma varchar(20) null,
    score varchar(20) null,
    title varchar(1000) null,
    ups varchar(20) null,
    upvote_ratio varchar(100) null,
    selftext varchar(5000) null,
    thumbnail varchar(300) null,
    domain varchar(100) null,
    created varchar(100) null

);
--
--             result_list.append({
--                 'resturant_name': restaurant_details_text,
--                 'link': url_text,
--                 'image': image_url,
--                 'price_category':price_category_text,
--                 'when_opened': when_opened_text,
--                 'restaurant_overview':restaurant_overview_text
--             })
create table scraping.yelp
(
    id int auto_increment
        primary key,
    created_at datetime default now() not null,
    resturant_name varchar(300) null,
    link varchar(1000) null,
    image varchar(1000) null,
    price_category varchar(100) null,
    when_opened varchar(100) null,
    restaurant_overview varchar(5000) null
);

create table scraping.cnn
(
    id int auto_increment
        primary key,
    created_at datetime default now() not null,
    category varchar(300) null,
    title varchar(1000) null,
    link varchar(1000) null
);
