from tools.log import Log


if __name__ == "__main__":
    #db = MySQL()
    #data = db.find("select * from wp_posts")
    #print(data)
    sql = "INSERT INTO `wp_posts` (`ID`, `post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) \
            VALUES(NULL , 1, '2017-04-09 22:39:35', '2017-04-09 14:39:35', '%s', '%s', '', 'inherit', 'closed', 'closed', '', '', '', '', '2017-04-09 22:39:35', '2017-04-09 14:39:35', '', 206, '', 0, 'revision', '', 0);"
    sql = sql % ("conent", "title")
    print(sql)
    Log().write_file(sql)
    #db.execute(sql)