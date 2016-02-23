
// ///

// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// var csrftoken = getCookie('csrftoken');

// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }

var url = 'check_int/'
var APIKEY = 'BNEBQIIL8KVC1LE'
var SECRET = 'YMX3GMBXS8ZDG3W'

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
                // console.log(result);
                errors = Object.keys(result.replacements)
                // console.log(errors)
                replacementsObject = result.replacements;
                // console.log(replacementsObject)

                $.each(errors, function(key, value){
                    // console.log(value)
                    if (replacementsObject[value] != 0) {
                        highlight_words(value, '.results p')
                    }
                    else {
                        underline_words(value, '.results p')
                    }
                });
            },
            error: function(result) {
                errorMsg = result['status']+' '+result['statusText']
                $('.results p').text(errorMsg);
            },
            beforeSend: function(jqXHR, settings) {
                //https://developers.google.com/maps/documentation/static-maps/get-api-key#dig-sig-key
                modUrl = settings.url.replace(/'/g, "%27") // chrome najwidoczniej nie escape'uje apostrofow...
                var signature = CryptoJS.HmacSHA1(modUrl, SECRET).toString(); 
                // console.log(signature)
                //jqXHR.setRequestHeader("Authorization", signature)

            }
        });
    });

    $(document).on('click','.highlight', function() {
        // console.log(replacementsObject)
        // console.log(this.id)
        replacements = replacementsObject[this.id]
        
        content = '<div id="replcontainer"><label>Czy miałes na myśli...</label><br><ul>'
        $.each(replacements, function(key, value){
            content = content + '<li>' + value + '</li>'
            // console.log(content)
        });

        content = content + '</ul></div>'
        $('.replacements #replcontainer').replaceWith(content);

    });

    function highlight_words(keywords, element) {
        if(keywords) {
            var textNodes;
            // console.log(keywords)
            var str = keywords.split(" ");
            // console.log('HERE')
            $(str).each(function() {
                var term = this;
                var textNodes = $(element).contents().filter(function() { return this.nodeType === 3 });
                textNodes.each(function() {
                    var content = $(this).text();

                // escape kodu html!
                content = content.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

                var regex = new RegExp('\\b'+term+'\\b', "gi");
                content = content.replace(regex, '<span id="'+ term +'" class="highlight">' + term + '</span>');

                // console.log(content)

                $(this).replaceWith(content);
            });
            });
        }
    }

    function underline_words(keywords, element) {
        if(keywords) {
            var textNodes;
            // console.log(keywords)
            var str = keywords.split(" ");
            // console.log(str)
            $(str).each(function() {
                var term = this;
                var textNodes = $(element).contents().filter(function() { return this.nodeType === 3 });
                textNodes.each(function() {
                    var content = $(this).text();

                    // escape kodu html!
                    content = content.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

                    var regex = new RegExp('\\b'+term+'\\b', "gi");
                    content = content.replace(regex, '<span id="'+ term +'" class="underline">' + term + '</span>');

                    $(this).replaceWith(content);
                });
            });
        }
    }
});    