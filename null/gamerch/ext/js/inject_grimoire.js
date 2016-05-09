chrome.extension.sendMessage({}, function (response) {
    var readyStateCheckInterval = setInterval(function () {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);

            var index = parseInt((localStorage["index"] || 0));

            var name;
            var prefix = 'カード_';
            var per = 2;

            try {
                name = /(editEntry|newEntry)\/([^\/]+)/.exec(location.pathname)[2];
            } catch (e) {
                name = null;
            }

            if ($('h1.notfound').length != 0) {
                location.href = "http://xn--cck1a4k5a.gamerch.com/gamerch/newEntry/" + encodeURI(prefix + data[index]['name'].replace("[", "【").replace("]", "】")) + "/normal_entry";
                return;
            }

            if (!name || decodeURI(name) != prefix + data[index]['name'].replace("[", "【").replace("]", "】")) {
                location.href = "http://xn--cck1a4k5a.gamerch.com/gamerch/editEntry/" + encodeURI(prefix + data[index]['name'].replace("[", "【").replace("]", "】"));
                return;
            }

            localStorage["index"] = index + per;

            wikiInputCard(index);
            dbSave();

            document.title = sprintf("%d / %d = %f", index + 1, data.length, (index + 1) / data.length);
        }
    }, 1);
});

function date2string(string) {
    var a = new Date(string);
    return a.getUTCFullYear() + '年' + a.getUTCMonth() + '月' + a.getUTCDay() + '日';
}

function dbSave() {
    $(".ui_btn_submit.js_ui_submit").click();
}

function wikiInputCharacter(index) {
    var tmpl = "\
*%s\n\
**プロフィール\n\
|!center:クラス|center:%s|\n\
|!center:年齢|center:%s|\n\
|!center:誕生日|center:%s|\n\
|!center:血液型|center:%s|\n\
|!center:身長|center:%s|\n\
|!center:体重|center:%s|\n\
|!center:スリーサイズ|center:B:%d W:%d H:%d|\n\
|!center:所属|center:%s|\n\
|!center:好きな食べ物|center:%s|\n\
|!center:嫌いな食べ物|center:%s|\n\
|!center:趣味|center:%s|\n\
|!center:特技|center:%s|\n\
|!center:在学年数|center:%s|\n\
**カード\
";
    var body = $("*[name=entry_text]");

    body.val(sprintf(tmpl,
        data[index]['name'],
        data[index].classRoomName,
        data[index].age,
        date2string(data[index].birthDay),
        data[index].blood,
        data[index].height,
        data[index].weight,
        data[index].bust, data[index].waist, data[index].hip,
        data[index].club,
        data[index].likeFood,
        data[index].hateFood,
        data[index].hobby,
        data[index].specialSkill,
        data[index].enrollmentPeriod
    ))
}

function wikiInputCard(index) {
    var tmpl = "\
*%s\n\
**%s\n\
|!center:クラス|center:%s|\n\
|!center:最大Lv|center:%d|\n\
|!center:コスト|center:%d|\n\
|!center:売値|center:%d|\n\
\n\
|~center:|center:初期|center:最大|\n\
|!center:攻撃|center:%d|center:%d|\n\
|!center:防御|center:%d|center:%d|\n\
\n\
|~center:スキル|center:最大Lv|\n\
|center:%s|center:%s|\n\
**%s+\n\
|!center:クラス|center:%s|\n\
|!center:最大Lv|center:%d|\n\
|!center:コスト|center:%d|\n\
|!center:売値|center:%d|\n\
\n\
|~center:|center:初期|center:最大|\n\
|!center:攻撃|center:%d|center:%d|\n\
|!center:防御|center:%d|center:%d|\n\
\n\
|~center:スキル|center:最大Lv|\n\
|center:%s|center:%s|\n\
";
    var body = $("*[name=entry_text]");
    var rare;

    switch (data[index].rarityType) {
        case 1:
        case 2:
            rare = 'N';
            break;

        case 11:
        case 12:
            rare = 'R';
            break;

        case 21:
        case 22:
            rare = 'SR';
            break;

        case 31:
        case 32:
            rare = 'SSR';
            break;
    }

    body.val(sprintf(tmpl,
        data[index]['name'],
        rare,
        data[index].classRoomName,
        data[index].maxLevel,
        data[index].cost,
        data[index].soldPrice,
        data[index].initialOffense, data[index].maxOffense,
        data[index].initialDefense, data[index].maxDefense,
        data[index].skillName, data[index].cardBattleSkillMaxLevel,
        rare,
        data[index + 1].classRoomName,
        data[index + 1].maxLevel,
        data[index + 1].cost,
        data[index + 1].soldPrice,
        data[index + 1].initialOffense, data[index + 1].maxOffense,
        data[index + 1].initialDefense, data[index + 1].maxDefense,
        data[index + 1].skillName, data[index + 1].cardBattleSkillMaxLevel
    ));
}
