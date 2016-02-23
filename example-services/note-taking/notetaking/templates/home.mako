# -*- coding: utf-8 -*- 
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>${project}, ${len(messages)} notes</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="${request.static_url('notetaking:static/css/bootstrap.css')}" rel="stylesheet" media="screen">
    
  </head>
  <body>
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">CRDT Note Taking</a>
        </div>
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav navbar-right">
            <button type="button" class="btn btn-primary navbar-btn" data-toggle="modal" data-target="#myModal">
              <span class="glyphicon glyphicon-edit" aria-hidden="true"></span>
            </button>
          </ul>
        </div>
      </div>
    </nav>
	  <div class=container>
      <table class="table table-condensed table-hover">
        <thead>
          <tr>
            <th>Note</th>
            <th>Date</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          % for msg in messages: 
          <tr>
            <td width="55%">${msg['content']}</td>
            <td width="25%">${msg['timestamp']}</td>
            <td width="5%">
            <form action="delete" method="POST">
            <button type="submit" name="msgid" value="${msg['msgid']}" class="close">&times;</button>
            </form></td>
          </tr>
          % endfor  
        </tbody>
      </table>
	  </div>	

    <!-- Modal -->
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <form action="compose" method="POST" role="form">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="myModalLabel">Add Note</h4>
          </div>
          <div class="modal-body">
            
              <div class="form-group">
                <label for="msgfield">Note</label>
                <textarea class="form-control" rows="3" id="msgfield" name="msgfield"></textarea>
              </div>
              <div class="form-group">
                <label for="fromfield">From</label>
                <input type="text" class="form-control" id="fromfield" name="fromfield" placeholder="${hostname}" disabled>
              </div>
            
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
          </form>
        </div>
      </div>
    </div>

    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="${request.static_url('notetaking:static/js/bootstrap.min.js')}"></script>
  </body>
</html>