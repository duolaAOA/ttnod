var Pagination = function Pagination(obj) {
    var totalCount = parseInt(obj.totalCount || 10000),     // 一共页数
    pageSize = parseInt(obj.pageSize || 10),                // 页大小
    buttonSize = parseInt(obj.buttonSize || 10),        // 按钮数
    pageParam = obj.pageParam || "page",            // 页码参数名
    className = obj.className || "pagination",      // 分页样式
    prevButton = obj.prevButton || "&laquo;",       // 前一页
    nextButton = obj.nextButton || "&raquo;",
    firstButton = obj.firstButton || "",
    lastButton = obj.lastButton || "";
    if (Pagination.getParam = function(a) {
        var t = new RegExp("(^|&)" + a + "=([^&]*)(&|$)", "i"),
        e = window.location.search.substr(1).match(t);
        return null != e ? decodeURI(e[2]) : null
    },
    Pagination.replaceUrl = function(name, value) {
        var oUrl = window.location.href.replace(window.location.hash, ""),
        reg = new RegExp("(^|&)(" + name + "=)([^&]*)(&|$)", "i"),
        r = window.location.search.substr(1).match(reg);
        return null != r ? oUrl.replace(eval("/" + r[0] + "/g"), r[1] + r[2] + value + r[4]) : oUrl + (oUrl.indexOf("?") > 0 ? "&": "?") + name + "=" + value
    },
    0 == totalCount || totalCount <= pageSize) return "";
    var page = parseInt(Pagination.getParam(pageParam)) || 0;
    page = page > 1 ? page: 1;
    var str = '<nav style="text-align: center"><ul class="' + className + '">';
    firstButton && (str += '<li class="page-item"><a class="page-link" href="' + Pagination.replaceUrl(pageParam, 1) + '">' + firstButton + "</a></li>"),
    str += page <= 1 ? '<li class="page-item disabled"><span class="page-link">' + prevButton + "</span></li>": '<li class="page-item"><a class="page-link" href="' + Pagination.replaceUrl(pageParam, page - 1) + '">' + prevButton + "</a></li>";
    var max = Math.ceil(totalCount / pageSize),
    start = Math.floor((page - 2) / (buttonSize - 2)) * (buttonSize - 2);
    start = start + buttonSize > max ? max - buttonSize: start,
    start = start >= 0 ? start: 0;
    for (var i = start + 1; i <= start + buttonSize && !(i > max || buttonSize < 3); i++) str += "<li" + (i == page ? ' class="active"': "") + '><a class="page-link" href="' + Pagination.replaceUrl(pageParam, i) + '">' + i + "</a></li>";
    return str += page >= max ? '<li class="page-item disabled"><span class="page-link">' + nextButton + "</span></li>": '<li class="page-item"><a class="page-link" href="' + Pagination.replaceUrl(pageParam, page + 1) + '">' + nextButton + "</a></li>",
    lastButton && (str += '<li class="page-item"><a class="page-link" href="' + Pagination.replaceUrl(pageParam, max) + '">' + lastButton + "</a></li></nav>"),
    str + "</ul>"
};