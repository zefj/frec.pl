var url = 'check_int/'

$(document).ready(function(){

    $('#post-form').on('submit', function(event){
        event.preventDefault();

        $('.replacements #replcontainer').empty();
        $('.results p').text('Przetwarzam...');

        var text = $('.blendy #text').val()
        var user = $('.blendy #user').val()
        var engine = $('.blendy input[type="radio"]:checked').val()
        
        $.ajax({
            type: "GET",
            url: url,
            data: {text: text, engine: engine},
            success: function(result) {
                $('.results p').text(text);
                errors = Object.keys(result.replacements)
                replacementsObject = result.replacements;
                console.log(result)
                $.each(errors, function(key, value){
                    if (replacementsObject[value] != 0) {
                        highlight_words(value, '.results p', 'highlight')
                    }
                    else {
                        highlight_words(value, '.results p', 'underline')
                    }
                });
            },
            error: function(result) {
                errorMsg = result['status']+' '+result['statusText']
                $('.results p').text(errorMsg);
            },
        });
    });

    $(document).on('click','.highlight', function() {
        replacements = replacementsObject[this.id]
        content = '<div id="replcontainer"><label>Czy miałes na myśli...</label><br><ul>'
        $.each(replacements, function(key, value){
            content = content + '<li>' + value + '</li>'
        });

        content = content + '</ul></div>'
        $('.replacements #replcontainer').replaceWith(content);

    });

    function highlight_words(keywords, element, action) {
        if(keywords) {
            var textNodes;
            var str = keywords.split(" ");

            $(str).each(function() {
                var term = this;
                var textNodes = $(element).contents().filter(function() { return this.nodeType === 3 });

                textNodes.each(function() {
                    var content = $(this).text();
                    content = content.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

                    var regex = new RegExp('(\\W|^)('+term+')(?=\\W|$)', "g");
                    // regex = new RegExp(term, "g");

                    if (action == 'highlight'){
                        content = content.replace(regex, '<span id="'+ term +'" class="highlight"> ' + term + '</span>');                       
                    }
                    else if (action == 'underline'){
                        content = content.replace(regex, '<span id="'+ term +'" class="underline">' + term + '</span>');
                    }

                    $(this).replaceWith(content);
                    
                });
            });
        }
    }
});    