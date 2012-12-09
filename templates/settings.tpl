{% include 'header.tpl' %}

    <div id="content">
        <form action='settings' method='post'>
        <table>
            <tr><td colspan=2><center>General Configuration</center></td></tr>
            <tr>
                <td>Port<br/><span style='font-size:small; color:red;'>Implemented on restart</span></td>
                <td><input type='text' name='port' value='{{port}}'></td>
            </tr>
            <tr><td colspan=2><center><input type='submit' value=' Submit ' name='submit'></center></td></tr>
            <tr><td colspan=2>Current Library Paths:</td></tr>
            {% for path in lib_paths %}
            <tr>
                <!-- {{path}} -->
                <td>{{path[0]}}</td>
                <td><center><button type='submit' name='remove' value='{{path[1]}}'> Remove </button></center></td>
            </tr>
            {% endfor %}     
            <tr style='padding-top:20px;'>
                <td>Add path to library:</td>
                <td><input type='text' name='add_dir'></td>
            </tr>
            <tr><td colspan=2><center><button type='submit' value='add' name='add'> Add </button></center></td></tr>
        </table>
    </div><!-- #footer -->


{% include 'footer.tpl' %}
