{% include 'header.tpl' %}

    <div id="content">
        <select name='playlist'>
            {% for list in playlists %}
            <option value='{{list[0]}}'>{{list[1]}}</option>
            {% endfor %}
        </select>
    </div><!-- #footer -->


{% include 'footer.tpl' %}
