$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });
});

hljs.configure({useBR: true});

$(document).ready(function() {
  $('p code').each(function(i, block) {
    hljs.highlightBlock(block);
  });
});