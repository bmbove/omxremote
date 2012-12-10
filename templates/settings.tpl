{% include 'header.tpl' %}

    <div id="content">
        <form action='settings' method='post'>
        <table>
            <tr><td colspan=2><center>General Configuration</center></td></tr>
            <tr>
                <td>Port<br/><span class='small_red'>Implemented on restart</span></td>
                <td><input type='text' name='port' value='{{config_dict['port']}}'></td>
            </tr>
	        <tr>
		        <td>Executable:</td>
		        <td><input type='text' name='executable' value='{{config_dict['executable']}}'></td>
	        </tr>
            
            <tr>
                <td>Pause: </td>
                <td><input type='text' name='pause_key' value='{{config_dict['pause_key']}}'></td>
            </tr>

            <tr>
                <td>Quit: </td>
                <td><input type='text' name='stop_key' value='{{config_dict['stop_key']}}'></td>
            </tr>

            <tr>
                <td>Vol Up: </td>
                <td><input type='text' name='vol_up_key' value='{{config_dict['vol_up_key']}}'></td>
            </tr>

            <tr>
                <td>Vol Down: </td>
                <td><input type='text' name='vol_down_key' value='{{config_dict['vol_down_key']}}'></td>
            </tr>

            <tr>
                <td>Fast Fwd: </td>
                <td><input type='text' name='ff_key' value='{{config_dict['ff_key']}}'></td>
            </tr>

            <tr>
                <td>Rewind: </td>
                <td><input type='text' name='rw_key' value='{{config_dict['rw_key']}}'></td>
            </tr>

            <tr>
		        <td>Cmd Line Args:</td>
		        <td><input type='text' name='cmd_args' value='{{config_dict['cmd_args']}}'></td>
	        </tr>
            <tr><td colspan=2><center><input type='submit' value=' Submit ' name='submit'></center></td></tr>
            <tr><td colspan=2>Current Library Paths:</td></tr>
            {% for path in lib_paths %}
            <tr>
                <!-- {{path}} -->
                <td style='padding-top:5px; padding-bottom:5px;border-bottom:1px solid black;'><span style='white-space:nowrap;font-size:x-small;'>
                    {{path[0]}}
                    {% if path[2] == 1 %}
                    <span class='small_red'>*R</span>
                    {% endif %}
                    </span>
                </td>
                <td style='border-bottom:1px solid black;'><center><button type='submit' name='remove' style='font-size:small;' value='{{path[1]}}'> Remove </button></center></td>
            </tr>
            {% endfor %}     
            <tr>
                <td style='padding-top:20px;'>Add path to library:</td>
                <td style='padding-top:20px;'><input type='text' name='add_dir'> <input type='checkbox' value='1' name='recurse' CHECKED> <span class='small_red'>Recursive</span></td>
            </tr>
            <tr><td colspan=2><center><button type='submit' value='add' name='add'> Add </button></center></td></tr>
        </table>
    </div><!-- #footer -->


{% include 'footer.tpl' %}
