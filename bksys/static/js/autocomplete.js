function loadSearch(){
    $('#search').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    }, {
        name: 'res',
        source: function(query, process) {
            $.ajax({
                type: 'POST',
                url: 'autocomplete/',
                dataType: 'json',
                async: false,
                data: 'search=' + $('#search').val(),
                success: function(data) {
                    return process(data);
                },
            });
        },
    });

    $('#search').on('typeahead:selected', function(e, datum) {
        show_room(datum);
    });
}
