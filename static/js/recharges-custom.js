function randomString(len) {
    len = len || 32;
    var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
    var maxPos = $chars.length;
    var pwd = '';
    for (i = 0; i < len; i++) {
        pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}


(function(document, window, $) {
    var datas = [];
    for (var i = 0; i < 1000; i++) {
        datas[i] = {
            "id": i ,
            "out_trade_no":randomString(32),
            "user": "admin" + i,
            "amount": i,
            "score": i,
            "status": "支付成功",
            "pay_type": "微信支付",
            "created_at": "2018-06-1" + i,
            "finished_at": "2018-08-1" + i,
            "msg": "{\"openid\": \"wxd930ea5d5a258f4f\", \"sub_mch_id\": null, \"cash_fee_type\": \"CNY\", \"settlement_total_fee\": \"301\", \"nonce_str\": \"KnFueXRQbEyYcw7JVdsovq6N9kLzG3rZ\", \"return_code\": \"SUCCESS\", \"err_code_des\": \"SUCCESS\", \"time_end\": \"20180720170444\", \"mch_id\": \"1353383502\", \"trade_type\": \"NATIVE\", \"trade_state_desc\": \"ok\", \"trade_state\": \"SUCCESS\", \"sign\": \"0A974E9BCF1BB6E79DDDA2215374DF80\", \"cash_fee\": \"301\", \"is_subscribe\": \"Y\", \"return_msg\": \"OK\", \"fee_type\": \"CNY\", \"bank_type\": \"CMC\", \"attach\": \"sandbox_attach\", \"device_info\": \"sandbox\", \"out_trade_no\": \"z-20180720162939-19472560\", \"transaction_id\": \"4914992017520180720170444323968\", \"total_fee\": \"301\", \"appid\": \"wxaac7ec0426a05c6c\", \"result_code\": \"SUCCESS\", \"err_code\": \"SUCCESS\"}"
        }
    }


// 分页查询参数，是以键值对的形式设置的
function queryParams(params) {
    return {
            limit: params.limit,
            page: (params.offset / params.limit) + 1,   //页码
            out_trade_no: $('#queryform input[name=\'tradeNo\']').val()
    }
}


    // 表格
    (function() {
        $('#rechargesTable').bootstrapTable({
            url: 'http://127.0.0.1:8008/trade/recharge/api/',
            method: 'get',
            dataType: "json",
            contentType:'application/x-www-form-urlencoded; charset=UTF-8',
            pageNumber: 1,
            //初始化加载第一页，默认第一页
            pagination: true,
            // 是否显示分页
            pageSize: 25,
            // 每页显示数量
            pageList: [10, 25, 50, 100, 200, 500, 1000],
            //可供选择的每页的行数（*）
            sidePagination: 'server',           // 服务端分页
            paginationLoop: false,          // 翻页循环
            queryParams:queryParams,//请求服务器时所传的参数
            cache : false, // 是否使用缓存
            toolbar: '#toolbar',
            //指定工具栏
            showRefresh: true,
            // 是否显示刷新按钮
            striped: true,
            //是否显示行间隔色
            clickToSelect: true,
            //是否启用点击选中行
            showColumns: true,
            // 是否显示所有列(显示的)
            showToggle: true,
            //是否显示详细视图和列表视图的切换按钮
            iconSize: 'outline',
            icons: {
                refresh: 'glyphicon-repeat',
                toggle: 'glyphicon-list-alt',
                columns: 'glyphicon-list'
            },

            showExport: true,  //是否显示导出按钮
            buttonsAlign:"left",  //按钮位置
            exportDataType: 'basic',   //导出的方式 all全部 selected已选择的  basic', 'all', 'selected'.
            Icons:'glyphicon-export icon-share',
            exportTypes:[ 'excel', 'doc', 'xlsx', 'csv', 'json' ],
            maintainSelected: true,             //设置为 true 在点击分页按钮或搜索按钮时，将记住checkbox（client使用）

            exportOptions:{
                      //ignoreColumn: [0,0],            //忽略某一列的索引
                      fileName: 'Recharges充值记录',              //文件名称设置
                      worksheetName: 'Sheet1',          //表格工作区名称
                      tableName: 'Recharges充值记录',
                      excelstyles: ['background-color', 'color', 'font-size', 'font-weight']
                  },

            columns: [
                {
                    field: 'check',
                    checkbox: true
                },
                {
                    field: 'id',
                    align: 'center',
                    width: '10',
                    formatter: function (value, row, index) {
                        return index + 1;
                    }
                },
                {
                    field: "out_trade_no",
                    width: '10',
                    align: 'center'
                },
                {
                    field: "user",
                    width: '10',
                    align: 'center'
                },
                {
                    field: "amount",
                    width: '10',
                    align: 'center'

                },
                {
                    field: "score",
                    width: '10',
                    align: 'center'

                },
                {
                    field: "status",
                    width: '10',
                    align: 'center'

                },
                {
                    field: "pay_type",
                    width: '10',
                    align: 'center'

                },
                {
                    field: "created_at",
                    width: '10',
                    align: 'center'

                },
                {
                    field: "finished_at",
                    width: '10',
                    align: 'center'

                },
                {
                    field: "msg",
                    width: '10',
                    align: 'left'

                }
            ]
        });

    })();
})(document, window, jQuery);