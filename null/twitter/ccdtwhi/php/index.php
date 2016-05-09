<?php

require_once 'include/meekrodb.2.2.class.php';

$result = "";
$updated = "";

$sql = "SELECT *, REPLACE(original_profile_image_url, 'pbs.twimg.com', 'pbs.twimg.com.nyud.net') as original_profile_image_url, from_unixtime(date, '%Y-%m-%d %H:%i:%s') as updated, from_unixtime(created_at, '%Y-%m-%d %H:%i:%s') as created, TRUNCATE((statuses_count + favourites_count + friends_count + followers_count) / Log(unix_timestamp(now()) - created_at), 2) AS kp FROM `tws` WHERE date = (SELECT date FROM `tws` GROUP BY date ORDER BY date DESC LIMIT 1) ORDER BY kp DESC LIMIT 100";

DB::$user = 'ccd';
DB::$password = '68XnJwc645CH6JpS';
DB::$dbName = 'ccd';
DB::$encoding = 'utf8';

$data = DB::query($sql);

$i = 1;

foreach ($data as $row) {
    $result = $result . '<tr><td>' . $i . '</td><td><p><a href="https://twitter.com/' . $row['screen_name'] . '"><img src="' . $row['original_profile_image_url'] .'" alt="@' . $row['screen_name'] . '" title="@' . $row['screen_name'] . '" height="48">' . htmlspecialchars($row['name'], ENT_QUOTES, 'UTF-8') . '</a></p></td><td>' . $row['kp'] . '</td><td>' . $row['statuses_count'] . '</td><td>' . $row['favourites_count'] . '</td><td>' . $row['friends_count'] . '</td><td>' . $row['followers_count'] . '</td><td>' . $row['created'] . '</td></tr>';
    $i++;
}

if($i != 1) {
    $updated = $data[0]['updated'];
}

?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>ツェーツェーデー Twitter 活用ランキング（仮）</title>
    <link rel="icon" href="favicon.ico">
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link href="css/jumbotron-narrow.css" rel="stylesheet">
</head>
<body>
<div class="container">
    <div class="header">
        <ul class="nav nav-pills pull-right">
            <li class="active"><a href="#">All</a></li>
            <li class="disabled"><a href="#">Daily</a></li>
            <li class="disabled"><a href="#">Weekly</a></li>
            <li class="disabled"><a href="#">Monthly</a></li>
            <li class="disabled"><a href="#">Yearly</a></li>
        </ul>
        <h3 class="text-muted">ツェーツェーデー Twitter 活用ランキング（仮）</h3>
    </div>
    <div class="row">
        <div class="col-xs-12">
            <h2>Statistics</h2>
            <div id="s_kp"></div>
        </div>
        <div class="col-xs-12">
            <h2>The Report: All</h2>
            <p>This report was generated on <?php echo $updated; ?> by ccdtws (0.1.0.1).</p>
            <table class="table table-hover table-striped">
                <thead>
                <tr>
                    <th>#</th>
                    <th>User</th>
                    <th>K.P.</th>
                    <th>Tweets</th>
                    <th>Favorites</th>
                    <th>Following</th>
                    <th>Followers</th>
                    <th>Created At</th>
                </tr>
                </thead>
                <tbody>
                <?php echo $result; ?>
                </tbody>
            </table>
        </div>
    </div>
    <div class="footer">
        <p><a href="https://twitter.com/bolezn">@bolezn</a></p>
    </div>
</div>
<script src="js/jquery-2.0.3.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="/js/highcharts.js"></script>
<script>
    $(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        var options = {
            chart: {
                renderTo: 's_kp',
                type: 'spline',
                zoomType: 'x'
            },
            title: {
                text: 'K.P.',
                x: -20
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'K.P.'
                }
            },
            credits: {
                enabled: false
            },
            legend: {
                enabled: false
            },
            tooltip: {
                crosshairs: true,
                shared: true
            },
            plotOptions: {
                spline: {
                    marker: {
                        enabled: false
                    }
                }
            },
            series: [{name: 'K.P.'}]
        };

        var url =  "http://c.miko.im/g_kp.php";
        $.getJSON(url,  function(data) {
            options.series[0].data = data;
            var chart = new Highcharts.Chart(options);
        });
    });
</script>
</body>
</html>
