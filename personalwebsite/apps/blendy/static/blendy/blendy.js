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

// substitution table for regex word boundary match. It needs a letter from [a-zA-Z], special characters including language specific characters 
// are not considered letters FOR SOME REASON. Ridiculous I even have to do this really.
var character_table = {       
    'ż':'CHARzDotCHAR',        
    'ź':'CHARzDashCHAR',        
    'ć':'CHARcDashCHAR',        
    'ń':'CHARnDashCHAR',        
    'ó':'CHARoDashCHAR',        
    'ł':'CHARlDashCHAR',        
    'ę':'CHAReTailCHAR',        
    'ą':'CHARaTailCHAR',        
    'ś':'CHARsDashCHAR',        
    'Ż':'CHARZDotCHAR',        
    'Ź':'CHARZDashCHAR',        
    'Ć':'CHARCDashCHAR',        
    'Ą':'CHARADashCHAR',        
    'Ś':'CHARSDashCHAR',        
    'Ę':'CHAREDashCHAR',        
    'Ł':'CHARLDashCHAR',        
    'Ó':'CHARODashCHAR',        
    'Ń':'CHARNDashCHAR',        
}

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

                    // Regex Word Boundaries do not work with special characters. Need a hack for exact match to work.
                    var parsedTerm = replace_special_characters(term)
                    var parsedContent = replace_special_characters(content)
                    var regex = new RegExp('\\b'+parsedTerm+'\\b', 'g')

                    if (action == 'highlight'){
                        content = parsedContent.replace(regex, '<span id="'+ parsedTerm +'" class="highlight">' + parsedTerm + '</span>');                       
                    }
                    else if (action == 'underline'){
                        content = parsedContent.replace(regex, '<span id="'+ parsedTerm +'" class="underline">' + parsedTerm + '</span>');
                    }

                    content = undo_character_replacement(content)
                    $(this).replaceWith(content);

                });
            });
        }
    }

    function replace_special_characters(string) {
        // replaces keyword special characters with substitutes from character_table
        $.each(character_table, function(key, value){
            regex = new RegExp(key, "g")
            string = string.replace(regex, value)
        })

        return string
    }

    function undo_character_replacement(string) {
        // restores content characters substitutions to original form
        $.each(character_table, function(key, value){
            regex = new RegExp(value, "g")
            string = string.replace(regex, key)
        })

        return string
    }
 
});    