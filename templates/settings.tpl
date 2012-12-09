{% include 'header.tpl' %}

    <div id="content">
        <form action='settings' method='post'>
        <table>
            <tr><td colspan=2><center>General Configuration</center></td></tr>
            <tr>
                <td>Port<br/><span class='small_red'>Implemented on restart</span></td>
                <td><input type='text' name='port' value='{{port}}'></td>
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
