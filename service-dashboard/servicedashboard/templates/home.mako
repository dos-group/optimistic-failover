# -*- coding: utf-8 -*- 
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>${project}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="${request.static_url('servicedashboard:static/css/bootstrap.css')}" rel="stylesheet" media="screen">
    <link href="${request.static_url('servicedashboard:static/css/custom.css')}" rel="stylesheet">
    <script type="text/javascript" src="${request.static_url('servicedashboard:static/js/jquery-1.11.3.js')}"></script>
    <script type="text/javascript" src="${request.static_url('servicedashboard:static/js/ajax.js')}"></script>
    
  </head>
  <body>
    
      <nav class="navbar navbar-default navbar-static-top">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#">Service Dashboard</a>
          </div>
          <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav navbar-right">
             
            </ul>
          </div>
        </div>
      </nav>
      <div class=container>
      <div class="panel panel-primary">
        <div class="panel-heading">Services</div>
        <div class="panel-body">

          <div class="row">
            % for service in services:   
            <div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
              % if service['running'] == 'False': 
              <div id="servicePanel${loop.index}" class="panel panel-danger">
              % else: 
              <div id="servicePanel${loop.index}" class="panel panel-success">
              % endif
                <div class="panel-heading">
                  ${service['type']}
                  <div class="dropdown" style="float:right;">
                    <button class="btn btn-default btn-xs"  id="dLabel${loop.index}" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                      <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dLabel${loop.index}">
                      <li><a href="/delservice/${loop.index}">Delete Service</a></li>
                      <li><a href="/instructions/stop/${loop.index}">Stop Service</a></li>
                      <li><a href="/instructions/start/${loop.index}">Start Service</a></li>
                    </ul>
                  </div>
                </div>
                <div class="panel-body">
                  <dl>
                    <dt>IP/Port</dt>
                    <dd>${service['ip']}</dd>
                    <dt>Host</dt>
                    <dd>${service['host']}</dd>                  
                  </dl>
                </div>
              </div>     
            </div>   
            % endfor
          </div>
          
        </div>
      </div>

      <div class="panel panel-primary">
        <div class="panel-heading">
          Virtual Servers

          <a class="btn btn-default btn-xs" style="float:right;" href="/vservers" id="vserver_refresh" role="button"><span class="text-right glyphicon glyphicon glyphicon-refresh "></span></a>
          <div class="clearfix"></div>
        </div>
        <div class="panel-body">

          <div class="row">
            % for server in vservers:                
            <div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">

              % if server['status_info'] == 'ACTIVE':
              <div class="panel panel-success" id="serverPanel_${server['id']}">
              % elif server['status_info'] == 'SHUTOFF':
              <div class="panel panel-default" id="serverPanel_${server['id']}">
              % else:
              <div class="panel panel-warning" id="serverPanel_${server['id']}">
              % endif
                <div class="panel-heading">
                  ${server['name']}
                  <div class="dropdown" style="float:right;">
                    <button class="btn btn-default btn-xs"  id="dLabel_${server['id']}" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                      <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dLabel_${server['id']}">
                      <li><a href="/vservers/start/${server['id']}">Start Instance</a></li>
                      <li><a href="/vservers/stop/${server['id']}">Shut Off Instance</a></li> 
                      <li><a href="/vservers/reboot/${server['id']}">Soft Reboot Instance</a></li>
                      <li role="separator" class="divider"></li>
                      <li><a href="/vservers/pause/${server['id']}">Pause Instance</a></li>
                      <li><a href="/vservers/unpause/${server['id']}">Unpause Instance</a></li>
                    </ul>
                  </div>
                </div>
                <div class="panel-body">
                  <dl>
                    <dt>Image</dt>
                    <dd>${server['os']}</dd>
                    <dt>IP</dt>
                    <dd id="serverIP_${server['id']}">${server['ip']}</dd>
                    <dt>Status</dt>
                    <dd id="serverStatus_${server['id']}">${server['status_info']}</dd>
                    <dt>CPU</dt>
                    <dd>
                      <div class="progress">
                        <div class="progress-bar progress-bar-info cpu-${server['id']}" role="progressbar" aria-valuenow="2" aria-valuemin="0" aria-valuemax="100" style="min-width: 0em; width: ${server['cpu']}%;">
                          <span class="show" id="cpu_${server['id']}">${server['cpu']}%</span>
                        </div>
                      </div>
                    </dd>
                    <dt>RAM</dt>
                    <dd>
                      <div class="progress">
                        <div  class="progress-bar progress-bar-warning ram-${server['id']}" role="progressbar" aria-valuenow="2" aria-valuemin="0" aria-valuemax="100" style="min-width: 0em; width: ${server['ram']}%;">
                           <span class="show" id="ram_${server['id']}">${server['ram']}%</span>
                        </div>
                      </div>

                    </dd>
                  
                  </dl>
                  
                    
                </div>
              </div>     
            </div>   
            % endfor
          </div>
          
        </div>
      </div>
	  </div>	

    <script src="${request.static_url('servicedashboard:static/js/bootstrap.min.js')}"></script>
  </body>
</html>
