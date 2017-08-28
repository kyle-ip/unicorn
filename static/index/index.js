/**
 * Created by c0hb1rd on 2017/7/26.
 */

$(".content-box-nav li").on("click", function () {
     $("li").removeClass("active-li");
     $(this).addClass("active-li")
});