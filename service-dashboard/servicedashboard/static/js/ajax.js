function refresh_cpu(){
    jQuery.ajax({
        url     : 'servers',
        type    : 'POST',
        dataType: 'json',
        success : function(data){
           
            for (i = 0; i < data.vservers.length; i++) {

                dcpu = document.getElementById("cpu_" + data.vservers[i].id.toString());
                dram = document.getElementById("ram_" + data.vservers[i].id.toString());
                sip = document.getElementById("serverIP_" + data.vservers[i].id.toString());
                sPanel = document.getElementById("serverPanel_" + data.vservers[i].id.toString());
                sStatus = document.getElementById("serverStatus_" + data.vservers[i].id.toString());

                if (dcpu == null) {
                    d = document.getElementById("vserver_refresh");
                    d.className = "btn btn-warning btn-xs";
                } else {

                    dcpu.innerHTML = data.vservers[i].cpu.toString() + '%';
                    $(".cpu-" + data.vservers[i].id.toString()).css('width', data.vservers[i].cpu.toString() + '%');

                    dram.innerHTML = data.vservers[i].ram.toString() + '%';
                    $(".ram-" + data.vservers[i].id.toString()).css('width', data.vservers[i].ram.toString() + '%');

                    sip.innerHTML = data.vservers[i].ip.toString();

                    sStatus.innerHTML = data.vservers[i].status_info.toString()
                    if (data.vservers[i].status_info === 'ACTIVE') {
                        sPanel.className = "panel panel-success";
                    } else if (data.vservers[i].status_info === 'SHUTOFF') {
                        sPanel.className = "panel panel-default";
                    } else if (data.vservers[i].status_info === 'TERMINATED') {
                        sPanel.className = "panel panel-warning";
                        d = document.getElementById("vserver_refresh");
                        d.className = "btn btn-warning btn-xs";
                    } else{
                        sPanel.className = "panel panel-warning";
                    }

                }
            }
        }
    });
    $('#cpubtn').button('reset')
}

function refresh_services(){
    jQuery.ajax({
        url     : 'services',
        type    : 'POST',
        dataType: 'json',
        success : function(data){
           
            for (i = 0; i < data.services.length; i++) {

                d = document.getElementById("servicePanel" + i.toString());
                if (data.services[i].running === 'True') {
                    d.className = "panel panel-success";
                } else {
                    d.className = "panel panel-danger";
                }
            }
        }
    });
}

setInterval(function(){
    refresh_cpu()
    refresh_services()
}, 1500);