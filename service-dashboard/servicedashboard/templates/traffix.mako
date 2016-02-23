      <!--
      <div class="row">
        <div class="col-md-6">
          <div class="panel panel-default">
            <div class="panel-heading">Insert Traffic Generation</div>
            <div class="panel-body">
              <p> An activated checkbox startes the insert traffic generation for the corresponding service. The traffic generation represents the composition of messages on that service.</p>
              <form action="save" method="POST">              
                % for service in services:
                <div class="checkbox">
                  <label>
                    <input type="checkbox" name="id${loop.index}" 
                    ${'checked' if service['traffic'] else ''}
                    value="True">
                    ${service['type']} on host ${service['host']}(${service['ip']})
                  </label>
                </div>
                % endfor
                <div class="form-group">
                  <div class="col-xs-offset-10 col-xs-1">
                    <button type="submit" class="btn btn-primary">Save</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="panel panel-default">
            <div class="panel-heading">Delete Traffic Generation</div>
            <div class="panel-body">
              <p> An activated checkbox startes the delete traffic generation for the corresponding service. The traffic generation represents the deletion of messages on that service.</p>
              <form action="dsave" method="POST">              
                % for service in services:
                <div class="checkbox">
                  <label>
                    <input type="checkbox" name="id${loop.index}" 
                    ${'checked' if service['traffic'] else ''}
                    value="True">
                    ${service['type']} on host ${service['host']}(${service['ip']})
                  </label>
                </div>
                % endfor
                <div class="form-group">
                  <div class="col-xs-offset-10 col-xs-1">
                    <button type="submit" class="btn btn-primary">Save</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      -->