{% include 'header.tpl' %}

    <div id="file_content">
        <form action='index' method='post'>
            {% for file in files %}
                <li class='filename'><a onclick="control('play', '{{file[0]|e}}')">{{file[1]|e}}</a>
                <hr>
            {% endfor %}
            
         </form>
    </div><!-- #footer -->


{% include 'footer.tpl' %}
