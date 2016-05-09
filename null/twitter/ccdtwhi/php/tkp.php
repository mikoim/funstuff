<?php
require_once 'include/meekrodb.2.2.class.php';

$sql = 'SELECT screen_name, name, statuses_count, favourites_count, friends_count, followers_count, TRUNCATE((statuses_count + favourites_count + friends_count + followers_count) / Log(unix_timestamp(now()) - created_at), 2) AS kp FROM tws WHERE date = (SELECT date FROM tws GROUP BY date ORDER BY date DESC LIMIT 1) ORDER BY kp DESC LIMIT 3';

DB::$user = 'ccd';
DB::$password = '68XnJwc645CH6JpS';
DB::$dbName = 'ccd';
DB::$encoding = 'utf8';

$data = DB::query($sql);

echo json_encode($data);