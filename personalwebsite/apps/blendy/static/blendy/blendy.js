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
            // beforeSend: function(jqXHR, settings) {
            //     //https://developers.google.com/maps/documentation/static-maps/get-api-key#dig-sig-key
            //     modUrl = settings.url.replace(/'/g, "%27") // chrome najwidoczniej nie escape'uje apostrofow...
            //     var signature = CryptoJS.HmacSHA1(modUrl, SECRET).toString(); 
            //     // console.log(signature)
            //     //jqXHR.setRequestHeader("Authorization", signature)

            // }
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

    var character_table12312 = {
        'ż':'\\u017C',
        'ź':'\\u017A',
        'ć':'\\u0107',
        'ń':'\\u0144',
        'ó':'\\u00F3',
        'ł':'\\u0142',
        'ę':'\\u0119',
        'ą':'\\u0105',
        'ś':'\\u015B',
        'Ż':'\\u017B',
        'Ź':'\\u0179',
        'Ć':'\\u0106',
        'Ą':'\\u0104',
        'Ś':'\\u015A',
        'Ę':'\\u0118',
        'Ł':'\\u0141',
        'Ó':'\\u00D3',
        'Ń':'\\u0143',
    }

    var character_table = {
        'ż':9,
        'ź':8,
        'ć':7,
        'ń':6,
        'ó':5,
        'ł':4,
        'ę':3,
        'ą':2,
        'ś':1,
    }

    function highlight_words(keywords, element, action) {
        if(keywords) {
            var textNodes;
            var str = keywords.split(" ");

            $(str).each(function() {
                var term = this;
                var orig_term = term;
                var textNodes = $(element).contents().filter(function() { return this.nodeType === 3 });

        /// FIX: IF LITERA IN KEYWORD

                for (var i = 0, len = term.length; i < len; i++) {
                    var c = term.charAt(i);
                    c_temp = c.toLowerCase();
                    if (character_table[c_temp] != undefined) {
                        c = c.toLowerCase();
                        regex = new RegExp(c, "gi");
                        term = term.replace(regex, character_table[c])
                    }
                }

                textNodes.each(function() {
                    var content = $(this).text();
                    console.log(content)
                    content = content.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

                    for (var i = 0, len = content.length; i < len; i++) {
                        var c = content.charAt(i);
                        c_temp = c.toLowerCase();
                        if (character_table[c_temp] != undefined) {
                            c = c.toLowerCase();
                            regex = new RegExp(c, "gi");
                            content = content.replace(regex, character_table[c])
                        }
                        
                    }

                    var regex = new RegExp('\\b'+term+'\\b', "g");

                    if (action == 'highlight'){
                        content = content.replace(regex, '<span id="'+ orig_term +'" class="highlight">' + orig_term + '</span>');                       
                    }
                    else if (action == 'underline'){
                        content = content.replace(regex, '<span id="'+ orig_term +'" class="underline">' + orig_term + '</span>');
                    }

                    $(this).replaceWith(content);
                });
            });
        }
    }

    // function underline_words(keywords, element) {
    //     if(keywords) {
    //         var textNodes;
    //         var str = keywords.split(" ");

    //         $(str).each(function() {
    //             var term = this;
    //             var orig_term = term;
    //             console.log(orig_term)
    //             var textNodes = $(element).contents().filter(function() { return this.nodeType === 3 });

    //             for (var i = 0, len = term.length; i < len; i++) {

    //                 var c = term.charAt(i);
    //                 c_temp = c.toLowerCase();
    //                 if (character_table[c_temp] != undefined) {
    //                     c = c.toLowerCase();
    //                     regex = new RegExp(c, "gi");
    //                     term = term.replace(regex, character_table[c])

    //                 }
                    
    //             }

    //             textNodes.each(function() {
    //                 var content = $(this).text();
    //                 content = content.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

    //                 for (var i = 0, len = content.length; i < len; i++) {
    //                     var c = content.charAt(i);
    //                     c_temp = c.toLowerCase();
    //                     if (character_table[c_temp] != undefined) {
    //                         c = c.toLowerCase();
    //                         regex = new RegExp(c, "gi");
    //                         content = content.replace(regex, character_table[c])
    //                     }
                        
    //                 }

    //                 var regex = new RegExp('\\b'+term+'\\b', "g");
    //                 content = content.replace(regex, '<span id="'+ orig_term +'" class="underline">' + orig_term + '</span>');

    //                 $(this).replaceWith(content);
    //             });
    //         });
    //     }
    // }
});    