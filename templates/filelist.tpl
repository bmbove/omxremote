{% include 'header.tpl' %}

    <div id="file_content">
            {% for file in files %}
               <button onclick="ajaxreq('pl_add', '{{file[0]}}')" name='add' vaue=''>+PL</button> <li class='filename'><a href='#' onclick="control('play', '{{file[0]|e}}')">{{file[1]|e}}</a>
                <hr>
            {% endfor %}
            
    </div><!-- #footer -->


{% include 'footer.tpl' %}
