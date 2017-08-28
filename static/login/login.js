/**
 * Created by c0hb1rd on 2017/7/25.
 */
$.getJSON('/api/get_qrcode', function (data) {
    $("#img").attr('src', data.image_url);
});

var interval_id;

interval_id = setInterval(function () {
    $.getJSON('/api/check_login', function (data) {
        if (1 === data.ok) {
            window.location.href = '/';
        }
        if (0 !== data.ok) {
            $("#msg").text(data.message)
        }
    })
}, 500);

function close() {
    clearInterval(interval_id);
}
