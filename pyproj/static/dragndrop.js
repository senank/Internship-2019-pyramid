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
    console.log(data)
    $.ajax({
        method: 'POST',
        data: data,
        url: $(this).data('update-url')
    });
});
