/**
 * Created by c0hb1rd on 2017/7/26.
 */

var content_box = $(".content-box");

function get_user_box(data) {
    return '' +
        '<section class="user-box">' +
        '<img title="{1}" src="{0}" alt="">'.format(data.image_url, data.nick_name) +
        '<section class="user-detail">' +
        '<ul>' +
        '<li title="{0}">{0}</li>'.format(data.nick_name) +
        '<li title="{0}">{0}</li>'.format(data.mark_name) +
        '<li class="user-sex fa {0}"></li>'.format(data.sex) +
        '<li title="{0}">{0}</li>'.format(data.signature) +
        '</ul>' +
        '</section>' +
        '</section>';
}


$.getJSON('/api/get_friends', function (data) {

    for (var index in data) {
        if (data.hasOwnProperty(index)) {
            var temp = get_user_box(data[index]);
            content_box.append(temp)
        }
    }
});


$("#submit").on("click", function () {
    document.getElementsByTagName("body")[0].focus();
    var message = $("#message").val();
        $.getJSON("/ctrl/change_text?msg={0}".format(message), function (data) {
            parent.layer.open({
            type: 1,
            skin: "fuckIt",
            anim: 1,
            title: "消息",
            shadeClose: true,
            content: 1 === data.ok ? '修改成功' : '修改失败',
            btn: '关闭',
            btnAlign: 'c'
        });
    });
});

$("#message").on("keypress", function (event) {
    if (13 === event.which) {
    document.getElementsByTagName("body")[0].focus();
    $("#submit").click();
}
});