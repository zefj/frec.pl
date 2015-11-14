$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
 	$('body').toggleClass('noscroll');
  });
});

hljs.configure({useBR: true});

$(document).ready(function() {
  $('p code').each(function(i, block) {
    hljs.highlightBlock(block);
  });
});

