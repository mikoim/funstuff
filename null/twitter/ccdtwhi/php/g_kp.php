<?php

require_once 'include/meekrodb.2.2.class.php';

$sql = "SELECT date as x, sum((statuses_count + favourites_count + friends_count + followers_count) / Log(unix_timestamp(now()) - created_at)) as y FROM tws where unix_timestamp(now()) - 604800 <= date group by date";

DB::$user = 'ccd';
DB::$password = '68XnJwc645CH6JpS';
DB::$dbName = 'ccd';
DB::$encoding = 'utf8';

$data = DB::query($sql);

$result = array();
$x = array();
$y = array();

foreach ($data as $row) {
    array_push($x, (float)$row['x'] * 1000);
    array_push($y, (float)$row['y']);
}

for($i = 1; $i < count($x); $i++) {
    array_push($result, array($x[$i], $y[$i] - $y[$i - 1]));
}

echo json_encode($result);