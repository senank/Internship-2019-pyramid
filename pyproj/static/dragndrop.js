var csrf_token = "${get_csrf_token()}";
$('.drag-events').sortable({
    axis: 'y',
    revert: true,
    // placeholder: "sortable-placeholder",
    cursor: "move",
    li: '.sortable'
}).on('sortupdate', function( event, ui ) {
    var position = 0,
        data = {};
    $(this).find('li input[data-id]').each(function(){
        data['id-' + $(this).data('id')] = position;
        position ++;
    });
    data.csrf_token = csrf_token;
    console.log(data)
    $.ajax({
        method: 'POST',
        data: data,
        //headers: csrf_token
        url: $(this).data('update-url')
    });
});
