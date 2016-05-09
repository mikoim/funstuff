chrome.extension.sendMessage({}, function (response) {
    var readyStateCheckInterval = setInterval(function () {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);

            /*
             if (location.pathname != "/gamerch/newEntry/%E6%96%B0%E3%81%97%E3%81%84DB%E3%83%9A%E3%83%BC%E3%82%B8/db_entry") {
             location.href = "http://schoolprincess.gamerch.com/gamerch/newEntry/%E6%96%B0%E3%81%97%E3%81%84DB%E3%83%9A%E3%83%BC%E3%82%B8/db_entry";
             return;
             }
             */

            //localStorage["index"] = 0;
            //return;

            var index = parseInt((localStorage["index"] || 0));

            /*
             if (data.length <= index) {
             localStorage["index"] = 0;
             index = 0;
             }
             */

            var name;

            try {
                name = /(editEntry|newEntry)\/([^\/]+)/.exec(location.pathname)[2];
            } catch (e) {
                name = null;
            }

            if (!name || decodeURI(name).replace("【", "[").replace("】", "]") != 'カード_' + data[index]['name']) {
                location.href = "http://schoolprincess.gamerch.com/gamerch/editEntry/" + encodeURI('カード_' + data[index]['name'].replace("[", "【").replace("]", "】"))
                //location.href = "http://schoolprincess.gamerch.com/gamerch/editEntry/" + data[index]['name'].replace("[", "【").replace("]", "】");
                return;
            }

            if ($('h1.notfound').length != 0) {
                location.href = "http://schoolprincess.gamerch.com/gamerch/newEntry/" + encodeURI('カード_' + data[index]['name'].replace("[", "【").replace("]", "】") + "/normal_entry");
                //location.href = "http://schoolprincess.gamerch.com/gamerch/newEntry/" + encodeURI(data[index]['name'].replace("[", "【").replace("]", "】") + "/db_entry");
                return;
            }

            localStorage["index"] = index + 1;

            /*
             if (data.length == index + 1) {
             alert("Finish!");

             localStorage["index"] = 0;
             return;
             }
             */

            wikiInput(index);
            //dbInput(index);
            dbSave();

            document.title = sprintf("%d / %d = %f", index + 1, data.length, (index + 1) / data.length);
        }
    }, 1);
});

function dbSave() {
    $(".ui_btn_submit.js_ui_submit").click();
}

function getCardImg(name, nf) {
    for (var i = 0; i < cards.length; i++) {
        if (name === cards[i].name) {
            return cards[i].image;
        }


    }

    return nf;
}

function wikiInput(index) {
    var tmpl = "\
*%s\n\
|~親密度1|親密度2|親密度3|親密度4|親密度5|\n\
|#ref(,200)|#ref(,200)|#ref(,200)|#ref(,200)|#ref(,200)|\n\
**基本情報\n\
|!レアリティ|center:%s|\n\
|!コスト|center:%d|\n\
|!最大Lv|center:%d|\n\
|!得意教科|center:%s|\n\
|!苦手教科|center:%s|\n\
|!属性|center:%s|\n\
|!所属|center:%s|\n\
**パラメータ\n\
|~|運動|知識|感性|\n\
|!初期|center:%d|center:%d|center:%d|\n\
|!最大||||\n\
**スキル\n\
|~|名称|効果|消費AP|回数制限|\n\
|!サポート|center:%s|center:%s|center:-|center:-|\n\
|!フロント|center:%s|center:%s|center:%s|center:%s|\n\
|!バック|center:%s|center:%s|center:%s|center:%s|\n\
**台詞\n\
|!親密度1|%s|\n\
|!親密度3|%s|\n\
|!親密度5|%s|\n\
";
    var body = $("*[name=entry_text]");

    var level;

    switch (data[index]['rarity_id']) {
        case 1:
            level = 40;
            break;
        case 2:
            level = 60;
            break;
        case 3:
            level = 80;
            break;
        case 4:
            level = 100;
            break;
        case 5:
            level = 120;
            break;
        case 6:
            level = 140;
            break;
    }

    body.val(sprintf(tmpl, data[index]['name'].replace("[", "【").replace("]", "】"),
        data[index].rarity_name, data[index].cost, level, data[index].good_subject, data[index].bad_subject, data[index].attribute, data[index].group_name,
        data[index].p_vit, data[index].p_int, data[index].p_chr,
        data[index].skill_name, data[index].skill_text,
        data[index].fskill, data[index].fskill_text, data[index].fskill_consume_point, data[index].fskill_limit_count,
        data[index].bskill, data[index].bskill_text, data[index].bskill_consume_point, data[index].bskill_limit_count,
        data[index].flavor_r1, data[index].flavor_r3, data[index].flavor_r5
    ))
}

function dbInput(index) {
    var cn = $("*[name=entry_name]");
    var rare = $("*[name=top_01]");
    var cost = $("*[name=top_02]");
    var maxLevel = $("*[name=top_05]");
    var goodSubject = $("*[name=top_04]");
    var badSubject = $("*[name=top_06]");
    var attribute = $("*[name=top_07]");
    var groupName = $("*[name=top_03]");

    var intV = $("*[name=middle_02]");
    var intI = $("*[name=middle_01]");
    var intC = $("*[name=middle_03]");

    var skillSupport = $("*[name=bottom_01]");
    var skillDescSupport = $("*[name=bottom_01_detail]");
    var skillFront = $("*[name=bottom_02]");
    var skillDescFront = $("*[name=bottom_02_detail]");
    var skillBack = $("*[name=bottom_03]");
    var skillDescBack = $("*[name=bottom_03_detail]");

    switch (data[index]['rarity_id']) {
        case 1:
            rare.val('10131');
            maxLevel.val('40');
            break;
        case 2:
            rare.val('10132');
            maxLevel.val('60');
            break;
        case 3:
            rare.val('10133');
            maxLevel.val('80');
            break;
        case 4:
            rare.val('10134');
            maxLevel.val('100');
            break;
        case 5:
            rare.val('10135');
            maxLevel.val('120');
            break;
        case 6:
            rare.val('12430');
            maxLevel.val('140');
            break;
    }

    cn.val(data[index]['name'].replace("[", "【").replace("]", "】"));
    cost.val(data[index]['cost']);
    goodSubject.val(data[index]['good_subject']);
    badSubject.val(data[index]['bad_subject']);
    attribute.val(data[index]['attribute']);
    groupName.val(data[index]['group_name']);

    intV.val(data[index]['p_vit']);
    intI.val(data[index]['p_int']);
    intC.val(data[index]['p_chr']);

    skillSupport.val(data[index]['skill_name']);
    skillDescSupport.val(data[index]['skill_text']);

    skillFront.val(data[index]['fskill']);
    if (data[index]['fskill_text'] != '') skillDescFront.val(data[index]['fskill_text'] + ' (' + data[index]['fskill_consume_point'] + 'AP / ' + data[index]['fskill_limit_count'] + '回迄)');
    else skillDescFront.val('');

    skillBack.val(data[index]['bskill']);
    if (data[index]['bskill_text'] != '') skillDescBack.val(data[index]['bskill_text'] + ' (' + data[index]['bskill_consume_point'] + 'AP / ' + data[index]['bskill_limit_count'] + '回迄)');
    else skillDescBack.val('');
}

var cards = [];
