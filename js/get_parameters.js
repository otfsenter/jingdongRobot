// 以下代码在订单结算页面的开发者工具Console中执行，用于获取必要的参数
//https://trade.jd.com/shopping/order/getOrderInfo.action

var eid = $('#eid').val();
var fp = $('#fp').val();
var trackId = $("#TrackID").val();
var riskControl = $('#riskControl').val();
console.log(`eid = ${eid}\nfp = ${fp}\ntrack_id = ${trackId}\nrisk_control = ${riskControl}`);
